# -*- coding:utf8 -*-

import json, requests
import sys

url='http://127.0.0.1:8888/WordEmbedding'
param = {"word":u'国', 'top_n': 5}
# param = {"word":sys.argv[1], 'top_n': sys.argv[2]}

param = json.dumps(param)

r = requests.post(url, files={'param': param})
json_data = json.loads(r.text, encoding='utf8')
print(json_data)

for key, value in json_data.iteritems():
    print(key)
    print(value)