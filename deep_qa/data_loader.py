#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Data Loader
'''
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 Guoxiu He. All Rights Reserved"
__author__    = "Guoxiu_he"
__date__      = "2017-08-08:18:32:05"

import os
import sys

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(curdir))
print(curdir)

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")

from keras.preprocessing.sequence import pad_sequences
import insuranceqa_data as insuranceqa

class Data_Loader(object):
    def __init__(self):
        print("Data loading...")

    def load(self):
        print("load train data, valid data, test_data and vocab data...")
        self._train_data = insuranceqa.load_pairs_train()
        self._test_data = insuranceqa.load_pairs_test()
        self._valid_data = insuranceqa.load_pairs_valid()
        self.vocab_data = insuranceqa.load_pairs_vocab()

    def stat(self):
        print("stat the length of all dataset...")
        self.max_len_train_question = 42
        self.max_len_valid_question = 31
        self.max_len_test_question = 33

        self.max_len_train_utterance = 878
        self.max_len_valid_utterance = 878
        self.max_len_test_utterance = 878

        self.average_len_train_question = 5
        self.average_len_valid_question = 5
        self.average_len_test_question = 5

        self.average_len_train_utterance = 162
        self.average_len_valid_utterance = 165
        self.average_len_test_utterance = 161

        self.vocab_size = 24997

    def show(self):
        print('type of train data', type(self._train_data))
        print('len of train data', len(self._train_data))

        print('type of valid data', type(self._valid_data))
        print('len of valid data', len(self._valid_data))

        print('type of test data', type(self._test_data))
        print('len of test data', len(self._test_data))

        for x in self._test_data:
            print('type of question', type(x['question']))
            print('type of utterance', type(x['utterance']))
            print('type of label', type(x['label']))
            print('index %s value: %s ++$++ %s ++$++ %s'
                  %(x['qid'], x['question'], x['utterance'], x['label']))
            break

    def pad(self):
        print("padding...")
        print("keys", self.vocab_data.keys())
        vocab_size = len(self.vocab_data['word2id'].keys())
        print("vocab size", vocab_size)
        VOCAB_PAD_ID = vocab_size + 1
        VOCAB_GO_ID = vocab_size + 2
        self.vocab_data['word2id']['<PAD>'] = VOCAB_PAD_ID
        self.vocab_data['word2id']['<GO>'] = VOCAB_GO_ID
        self.vocab_data['id2word'][VOCAB_PAD_ID] = '<PAD>'
        self.vocab_data['id2word'][VOCAB_GO_ID] = '<GO>'

    def process(self):
        print("processing for train data, valid data and test data...")
        train_question, train_utterance, train_label = [], [], []
        valid_question, valid_utterance, valid_label = [], [], []
        test_question, test_utterance, test_label = [], [], []

        for train in self._train_data:
            train_question.append(train['question'])
            train_utterance.append(train['utterance'])
            train_label.append(train['label'])

        for valid in self._valid_data:
            valid_question.append(valid['question'])
            valid_utterance.append(valid['utterance'])
            valid_label.append(valid['label'])

        for test in self._test_data:
            test_question.append(test['question'])
            test_utterance.append(test['utterance'])
            test_label.append(test['label'])

        return (pad_sequences(train_question, maxlen=self.max_len_train_question),
                pad_sequences(train_utterance, maxlen=self.max_len_train_utterance),
                train_label), \
               (pad_sequences(valid_question, maxlen=self.max_len_train_question),
                pad_sequences(valid_utterance, maxlen=self.max_len_train_utterance),
                valid_label), \
               (pad_sequences(test_question, maxlen=self.max_len_train_question),
                pad_sequences(test_utterance, maxlen=self.max_len_train_utterance),
                valid_label)

def test():
    data_loader = Data_Loader()
    data_loader.load()
    data_loader.show()
    data_loader.pad()

if __name__ == '__main__':
    test()