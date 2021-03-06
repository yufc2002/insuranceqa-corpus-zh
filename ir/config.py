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
prvdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.dirname(curdir))

from elasticsearch import Elasticsearch

class Config(object):
    def __init__(self):
        print("config...")
        self.es = Elasticsearch(['localhost'], port=9200)
        self.index_name = "tk_qa_index"
        self.doc_type = "text"
        self.doc_path = prvdir+'/corpus/pairs/tk_pairs.json'

def main():
    Config()

if __name__ == "__main__":
    main()