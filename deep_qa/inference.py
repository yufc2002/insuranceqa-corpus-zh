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

import numpy as np
import jieba
from keras.preprocessing.sequence import pad_sequences

from data_loader import Data_Loader
from model import Network

from ir.search import Search
from ir.config import Config

class Inference(object):
    def __init__(self, model_path = './models/basic_baselineThu_Aug_17_01:40:41_2017.h5'):
        print("Inference...")
        self.model_path = model_path
        self.update_model_path = './models/basic_baselineMon_Aug_21_20:25:56_2017update.h5'
        self.max_len_train_question = 42
        self.max_len_train_utterance = 878

    def inference(self, model, question_list, utterance_list):
        result = model.predict([question_list, utterance_list], verbose=0)
        print('the result is:\n', result)
        first = [tmp[0] for tmp in result]
        best_index = first.index(max(first))
        return best_index

    def get_candidate(self, query, result, word2id):

        utterance_list = []
        query_list = []

        query_tmp = []
        for word in query.strip().split():
            try:
                query_tmp.append(word2id[word.decode('utf8')])
            except:
                pass

        for pair in result:
            question = pair[0].strip().split()
            utterance = pair[1].strip().split()
            print(''.join(question), ''.join(utterance))
            tmp = []
            for word in utterance:
                try:
                    tmp.append(word2id[word.decode('utf8')])
                except:
                    pass
            utterance_list.append(tmp)
            query_list.append(query_tmp)

        return pad_sequences(query_list, maxlen=self.max_len_train_question), pad_sequences(utterance_list, maxlen=self.max_len_train_utterance)

    def get_best_utterance(self, best_index, result):
        best_pair = result[best_index]
        question = ''.join(best_pair[0].strip().split())
        utterance = ''.join(best_pair[1].strip().split())
        print('最佳答案参照：', question, utterance)
        return question, utterance

    def pair_list_convert(self, pair_list, word2id):
        question_list = []
        utterance_list = []
        for pair in pair_list:
            question = pair[0].strip().split()
            utterance = pair[1].strip().split()
            question_tmp = []
            for word in question:
                try:
                    question_tmp.append(word2id[word.decode('utf8')])
                except:
                    pass
            utterance_tmp = []
            for word in utterance:
                try:
                    utterance_tmp.append(word2id[word.decode('utf8')])
                except:
                    pass
            question_list.append(question_tmp)
            utterance_list.append(utterance_tmp)
        question_list = pad_sequences(question_list, maxlen=self.max_len_train_question)
        utterance_list = pad_sequences(utterance_list, maxlen=self.max_len_train_utterance)
        return question_list, utterance_list

def Prepare():
    data_loader = Data_Loader()
    data_loader.load()
    data_loader.stat()
    word2id = data_loader.vocab_data['word2id']

    model = Network()
    model.info(data_loader)
    _, network_model = model.basic_baseline()

    config = Config()
    search = Search()

    inference = Inference()
    # network_model.load_weights(inference.model_path)
    network_model.load_weights(inference.update_model_path)
    return inference, network_model, config, search, word2id

def Process(inference, network_model, config, search, word2id, query, top_n):

    query = ' '.join(jieba.cut(query.strip(), cut_all=False))
    result = search.search_by_question(query, int(top_n), config)

    question_list, utterance_list = inference.get_candidate(query, result, word2id)
    best_index = inference.inference(network_model, question_list, utterance_list)

    question, utterance = inference.get_best_utterance(best_index, result)
    return question, utterance

def main():

    inference, network_model, config, search, word2id = Prepare()

    while True:

        query = raw_input("您想问什么 >> ")

        if query == 'EXIT':
            break

        top_n = raw_input("top n >> ")

        if not top_n:
            top_n = 3

        # query = ' '.join(jieba.cut(query.strip(), cut_all=False))
        # result = search.search_by_question(query, int(top_n), config)
        #
        # question_list, utterance_list = inference.get_candidate(query, result, word2id)
        # best_index = inference.inference(network_model, question_list, utterance_list)
        #
        # inference.get_best_utterance(best_index, result)

        Process(inference, network_model, config, search, word2id, query, top_n)

if __name__ == "__main__":
    main()