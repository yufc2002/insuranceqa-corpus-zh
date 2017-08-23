#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 Guoxiu He. All Rights Reserved"
__author__ = "Guoxiu He"
__date__ = "2017-08-08:18:32:05"

import sys, os
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(curdir))

# ===== 依赖导入 =====
import tornado.ioloop, tornado.web
import json

from utils import Utils

utils = Utils()
WordEmbeddingModel = utils.load_word_embedding()

class WordEmbeddingHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Please upload param by python script...')
        # self.write('''<html><head><title>Upload File</title></head><body>
        # <form action='IdCard' enctype="multipart/form-data" method='post'>
        # <input type='file' name='file'/><br/><input type='submit' value='submit'/>
        # </form></body></html>''')

    def post(self):
        files = self.request.files.get("param")
        param = files[0]['body'].strip()
        param = json.loads(param)
        word = param['word']
        top_n = int(param['top_n'])
        try:
            json_data = utils.get_topn_similarity_word(WordEmbeddingModel, word, top_n)
            json_data = json.dumps(json_data)
        except:
            json_data = '没有这个词'
        self.write(json_data)

def make_app():
    return tornado.web.Application([
        (r"/WordEmbedding", WordEmbeddingHandler)])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
