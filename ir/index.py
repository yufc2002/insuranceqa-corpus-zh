#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 Guoxiu He. All Rights Reserved"
__author__ = "Guoxiu He"
__date__ = "2017-08-08:18:32:05"

import codecs
import json
import jieba
from elasticsearch import helpers
from time import gmtime, strftime

import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
prvdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(curdir))

from config import Config


class Index(object):
    def __init__(self):
        print("create index...")
        self.word_dict_path = prvdir+'/corpus/pairs/word_dict'

    def jieba_load_word_dict(self):
        print("load word dict...")
        jieba.load_userdict(self.word_dict_path)

    def warning_with_time(self, warning_string):
        """
        generate warning info with time
        """
        return warning_string + "[" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + "]"

    def data_convert(self, file_path):
        print("convert metedata into format we need...")
        docs = {}
        with codecs.open(file_path, encoding='utf8') as f:
            for line in f.readlines():
                line = json.loads(line.strip(), encoding='utf8')
                iid = line['id']
                question = ' '.join(jieba.cut(line['question'].strip(), cut_all=False))
                utterance = ' '.join(jieba.cut(line['utterance'].strip(), cut_all=False))
                docs[iid] = {'question': question, 'utterance': utterance}
        print(self.warning_with_time("docs loaded"))
        return docs

    def create_index(self, config):
        print("creating '%s' index..." % (config.index_name))
        request_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "similarity": {
                    "LM": {
                    "type": "LMJelinekMercer",
                    "lambda": 0.4
                    }
                }
            },
            "mappings": {
                "text": {
                    "properties": {
                        "question": {
                            "type": "text",
                            "term_vector": "with_positions_offsets_payloads",
                            "store": True,
                            "analyzer": "standard",
                            "similarity": "LM"
                        },
                        "utterance": {
                            "type": "text",
                            "term_vector": "with_positions_offsets_payloads",
                            "store": True,
                            "analyzer": "standard",
                            "similarity": "LM"
                        }
                    }
                }
            }
        }
        config.es.indices.delete(index=config.index_name, ignore=[400, 404])
        res = config.es.indices.create(index=config.index_name, body=request_body)
        print(self.warning_with_time("index is created successfully!"))
        return res

    def bulk_index(self, docs, bulk_size, config):
        '''bulk indexing docs
        :param docs:
        :param bulk_size:
        :param config:
        :return:
        '''
        print("bulk index for docs...")
        count = 1
        actions = []
        for doc_id, doc in docs.items():
            action = {
                "_index": config.index_name,
                "_type": config.doc_type,
                "_id": doc_id,
                "_source": doc
            }

            actions.append(action)
            count += 1

            if len(actions) % bulk_size == 0:
                helpers.bulk(config.es, actions)
                print(self.warning_with_time("bulk index: " + str(count)))
                actions = []

        if len(actions) > 0:
            helpers.bulk(config.es, actions)
            print(self.warning_with_time("bulk index: " + str(count)))

def main():
    config = Config()
    index = Index()
    index.jieba_load_word_dict()
    docs = index.data_convert(config.doc_path)
    print(docs[1])
    print(type(docs))
    res = index.create_index(config)
    index.bulk_index(docs, 100, config)

if __name__ == "__main__":
    main()