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

from deep_qa.inference import Prepare, Process

Inference, Network_model, Config, Search, Word2id = Prepare()

class TKQAHandler(tornado.web.RequestHandler):

    def get(self):
        self.render(curdir+'/views/index.html')
        # self.render('./views/qa.html')

    def post(self):
        self.use_write()

    def use_render(self):
        query = self.get_argument('query')
        top_n = int(self.get_argument('top_n'))
        try:
            question, utterance = Process(Inference, Network_model, Config, Search, Word2id, query, top_n)
            json_data = {'question': question, 'utterance': utterance}
            self.render(curdir+'/views/answer.html',
                        query=query,
                        question=json_data['question'],
                        utterance=json_data['utterance'])
        except:
            json_data = '没有这个词'
            self.write(json_data)

    def use_write(self):
        query = self.get_argument('query')
        top_n = int(self.get_argument('top_n'))
        try:
            question, utterance = Process(Inference, Network_model, Config, Search, Word2id, query, top_n)
            json_data = {'question': question, 'utterance': utterance}
            self.write(json.dumps(json_data))
        except:
            json_data = '没有这个词'
            self.write(json_data)

def make_app():
    return tornado.web.Application([
        (r"/TKQA", TKQAHandler)])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
