#-*- coding: utf-8 -*-
from config import *
from time import gmtime, strftime
from elasticsearch import helpers


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
    
    for doc in res["hits"]["hits"]:
        score_1 = doc["_score"]
        
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
        score_2 += doc["_score"] * sim(target_iid, iid)
    
    score = (1-alpha)*score_1 + alpha*score_2
    return score
    


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

def get_df_by_tag(tag):
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
        return res["term_vectors"]["tags"]["terms"][tag]["doc_freq"]
    except:
        return

if __name__ == '__main__':

    print get_df_by_tag('sky')

    # res = original_score_on_subsets(query="cloud sky", iids=["1","2","3"])
    # print(res)

# get_df

# 14/30 公式
# input: tag, id_list

# 利用第一个方法
# query
# id of image
# 规划
# 上课读论文，
# 事情分轻重缓急
# 提高代码能力
# 实验室工作分时间。。
# 有计划完成各种代码的目标
# 论文每天修改计划