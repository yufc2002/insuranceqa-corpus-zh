#-*- coding: utf-8 -*-
from config import *
from time import gmtime, strftime
from elasticsearch import helpers
from collections import Counter
import numpy as np

##### search function #####
def separate_score_function(query, target_iid, similar_iids, alpha=0.5):
    """
    输入
        - query, 查询字符串
        - target_iid, 目标图片D
        - similar_iids, 拓展图片集合R_D
    输出
        - score，论文公式 (1)+(4)
    """
    # 计算公式(1)第一部分
    q1 = {"query": 
            {"bool":
                {"must": 
                    {"match": 
                        {"tags": query
                        }
                    },
                "filter":
                    {"term": 
                        {"_id": target_iid
                        }
                    }
                }
            }
        }
    res = ES.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=q1)

    score_1 = [doc for doc in res["hits"]["hits"]][0]["_score"]

    # 用公式(4)计算公式(1)第二部分
    q2 = {"query": 
            {"bool":
                {"must": 
                    {"match": 
                        {"tags": query
                        }
                    },
                "filter":
                    {"terms": 
                        {"_id": iids
                        }
                    }
                }
            }
        }
    res = ES.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=q2)
    score_2 = 0
    for doc in res["hits"]["hits"]:
        iid = doc["_id"]
        score_2 += doc["_score"] * vis_sim(target_iid, iid)

    score = (1-alpha)*score_1 + alpha*score_2
    return score

def merge_score_function(query, target_iid, similar_iids, alpha=0.5):
    """
    输入
        - query, 查询字符串
        - target_iid, 目标图片D
        - similar_iids, 拓展图片集合R_D
    输出
        - score，论文公式 (1)+(3)
    """
    # 计算公式(1)第一部分
    q1 = {"query": 
            {"bool":
                {"must": 
                    {"match": 
                        {"tags": query
                        }
                    },
                "filter":
                    {"term": 
                        {"_id": target_iid
                        }
                    }
                }
            }
        }
    res = ES.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=q1)

    score_1 = [doc for doc in res["hits"]["hits"]][0]["_score"]

    # 获取相似图片的所有tags
    texts = []
    unique_tags = []
    for iid in similar_iids:
        unique_tags += get_tags_by_id(iid).split()
        texts.append(get_tags_by_id(iid))
    unique_tags = list(set(unique_tags))

    # 用公式(3)计算公式(1)第二部分
    score_2 = 0
    for w in query.split():
        a = 0  # 分子
        for iid, text in similar_iids, texts:
            a += count_tag_freq(w, text) * vis_sim(target_iid, iid)
        b = 0  # 分母
        for t in unique_tags:
            for iid, text in similar_iids, texts:
                b += count_tag_freq(t, text) * vis_sim(target_iid, iid)
        score_2 += a/b

    score = (1-alpha)*score_1 + alpha*score_2
    return score

def score_function(query, target_iid, similar_iids):
    """
    输入
        - query, 查询字符串
        - target_iid, 目标图片D
        - similar_iids, 拓展图片集合R_D
    输出
        - score，论文公式 (5)
    """
    score = 0
    for word in query.split():
        for tag in get_tags_by_id(target_iid).split():
            for iid, text in similar_iids, texts:
                part1 = 0.5 + 0.5 * max((get_tf_and_sum(tag, similar_iids)[0]/float(get_tf_and_sum(tag, similar_iids)[1])-get_ttf_by_tag(tag)/float(get_sum_ttf_by_tag(tag))), 0)
                score += part1
    part2 = 1.0 + np.log(N/(1+len(get_iids_by_tag(tag))))
    part3 = 1.0 / np.sqrt(len(get_tags_by_id(target_iid).split()))
    part4 = get_tf_and_sum(tag, get_iids_by_tag(tag))[0]/float(get_tf_and_sum(tag, get_iids_by_tag(tag))[1])
    return score * part2 * part3 * part4

def count_tag_freq(tag, text):
    tmp_tags = text.split()
    freq = Counter(tmp_tags).get(tag, 0)
    return freq

def get_tf_and_sum(tag, similar_iids):
    # 获取一个tag的tf和tag总数
    unique_tags = []
    tf = 0
    for iid in similar_iids:
        unique_tag = get_tags_by_id(iid).split()
        unique_tags += unique_tag
        tf += Counter(unique_tag).get(tag, 0)
    tf_sum = len(unique_tags)
    return tf, tf_sum

def original_score_on_subsets(query, iids):
    """
    输入
        - query, 查询字符串
        - iids, 需要查询的图像编号列表
    输出
        - iid_score_pairs, 图像编号和得分对列表，列表中每个元素是一个(iid, score)。
    """
    q = {"query": 
            {"bool":
                {"must": 
                    {"match": 
                        {"tags": query
                        }
                    },
                "filter":
                    {"terms": 
                        {"_id": iids
                        }
                    }
                }
            }
        }
    res = ES.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=q)
    iid_score_pairs = []
    for doc in res["hits"]["hits"]:
        iid = doc["_id"]
        score = doc["_score"]
        # tags = doc["_source"]["tags"]
        iid_score_pairs.append((iid, score))
    return iid_score_pairs

def get_tags_by_id(iid):
    """get all tags of image by image id
    output is a string (tag1 tag2 tag3 ...)
    """
    res = ES.get(index=INDEX_NAME, doc_type=DOC_TYPE, id=iid)
    text = res["_source"]["tags"]
    return text

def bulk_index(docs, bulk_size, count):
    """bulk indexing docs"""
    actions = []
    for doc_id, doc in docs.items():
        action = {
            "_index": INDEX_NAME,
            "_type": DOC_TYPE,
            "_id": doc_id,
            "_source": doc
        }

        actions.append(action)
        count += 1

        if len(actions) % bulk_size == 0:
            helpers.bulk(ES, actions)
            print(warning_with_time("bulk index: "+str(count)))
            actions = []

    if len(actions) > 0:
        helpers.bulk(ES, actions)
        print(warning_with_time("bulk index: " + str(count)))
        actions = []

##### other function #####
def warning_with_time(warning_string):
    """
    generate warning info with time
    """
    return warning_string + "[" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + "]"

def get_iids_by_tag(tag):
    # 通过tag获得相关列表
    q = {"query": 
            {"bool":
                {"must": 
                    {"match": 
                        {"tags": tag
                        }
                    }
                }
            }
        }
    res = ES.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=q)
    iids = []
    for doc in res["hits"]["hits"]:
        iid = doc["_id"]
        iids.append(iid)
    return iids

def get_termvectors(tag):
    # 获取tag的相关统计
    q = {"query": 
            {"bool":
                {"must": 
                    {"match": 
                        {"tags": tag
                        }
                    }
                }
            }
        }
    res = ES.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=q)
    # print res
    iid_score_pairs = []
    for doc in res["hits"]["hits"]:
        iid = doc["_id"]
        score = doc["_score"]
        # tags = doc["_source"]["tags"]
        iid_score_pairs.append((iid, score))
    try:
        iid, score = iid_score_pairs[0]
        # body = {'query': {'match': {'tags': tag}}}
        # res = ES.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=body)
        # res = ES.mtermvectors(index=INDEX_NAME, doc_type=DOC_TYPE, body=body, term_statistics=True)
        res = ES.termvectors(index=INDEX_NAME, doc_type=DOC_TYPE, id=iid, term_statistics=True, field_statistics=True)
        # return res["term_vectors"]["tags"]["terms"][tag]["doc_freq"]
        return res
    except:
        return None

def get_df_by_tag(tag):
    # 通过tag获得该tag的df
    try:
        res = get_termvectors(tag)
        return res["term_vectors"]["tags"]["terms"][tag]["doc_freq"]
    except:
        return None

def get_tf_by_tag(tag):
    # 通过tag获得该tag的tf
    try:
        res = get_termvectors(tag)
        return res["term_vectors"]["tags"]["terms"][tag]["term_freq"]
    except:
        return None

def get_ttf_by_tag(tag):
    # 通过tag获得该tag的总频次
    try:
        res = get_termvectors(tag)
        return res["term_vectors"]["tags"]["terms"][tag]["ttf"]
    except:
        return None

def get_sum_ttf_by_tag(tag):
    # 通过tag获得所有的tag总数
    try:
        res = get_termvectors(tag)
        return res["term_vectors"]["tags"]["field_statistics"]["sum_ttf"]
    except:
        return None

if __name__ == '__main__':

    print get_ttf_by_tag('sky')
    # print get_termvectors("sky")

    # res = original_score_on_subsets(query="cloud sky", iids=["1","2","3"])
    # print(res)