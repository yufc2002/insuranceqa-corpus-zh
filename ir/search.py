#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 Guoxiu He. All Rights Reserved"
__author__ = "Guoxiu He"
__date__ = "2017-08-08:18:32:05"

import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(curdir))

import jieba

from config import Config

class Search(object):
    def __init__(self):
        print("Search what I want...")

    def search_by_question(self, query, top_n, config):
        q = {"query":
                 {"bool":
                      {"must":
                           {"match":
                                {"question": query}
                           }
                       }
                 }
             }
        # res = config.es.get(index=config.index_name, doc_type=config.doc_type, id=10)
        # res = config.es.search(index=config.index_name, doc_type=config.doc_type, body={"query": {"match_all": {}}})
        res = config.es.search(index=config.index_name, doc_type=config.doc_type, body=q)
        # print(res)
        topn = res['hits']['hits']
        count = 0
        result = []
        for data in topn:
            if count < top_n:
                result.append((data['_source']['question'], data['_source']['utterance']))
                count += 1
        return result

def main():
    config = Config()
    search = Search()
    query = '介绍下微保？'
    query = ' '.join(jieba.cut(query.strip(), cut_all=False))
    result = search.search_by_question(query, 4, config)
    for data in result:
        print(data[0], data[1])

if __name__ == '__main__':
    main()