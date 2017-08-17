#-*- coding: utf-8 -*-
from elasticsearch import Elasticsearch

##### Setup configs here
# set elasticsearch localhost and port
ES = Elasticsearch(['localhost'], port=9200)
# set index name
INDEX_NAME = "test_yahoo_1m_tags"
# set doc type
DOC_TYPE = "text"