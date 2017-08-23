# -*- coding:utf8 -*-

import json, requests

url='http://202.114.66.181:8888/TKQA'
# url='http://192.168.1.125:8888/TKQA'
param = {"query":u'微医保是什么？', 'top_n': 3}
# param = {"word":sys.argv[1], 'top_n': sys.argv[2]}

r = requests.post(url, data=param)
print(r.text)
json_data = json.loads(r.text)
print('question:')
print(json_data['question'])
print('utterance:')
print(json_data['utterance'])