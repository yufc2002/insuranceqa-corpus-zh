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

import gensim

class Utils(object):
    def __init__(self):
        print("let's use utils...")
        self.wordvecs_txt = '../corpus/embedding/wordvecs.txt'
        self.wordvecs_vcb = '../corpus/embedding/wordvecs.vcb'
        self.word_embedding = '../corpus/embedding/word_embedding.bin'

    def convert2bin(self):
        print("convert old embedding format to normal format...")
        text = open(self.wordvecs_txt, 'r')
        vcb = open(self.wordvecs_vcb, 'r')
        fw = open(self.word_embedding, 'a')
        fw.write('210437'+' '+'64'+'\n')
        while True:
            vec = text.readline()
            word = vcb.readline()
            if not word:
                return
            word = word.strip()
            vec = vec.strip().split(',')
            fw.write(word+' '+' '.join(vec)+'\n')
        text.close()
        vcb.close()
        fw.close()

    def load_word_embedding(self):
        print("load word embedding model...")
        word_embedding = gensim.models.KeyedVectors.load_word2vec_format(self.word_embedding)
        return word_embedding

    def get_topn_similarity_word(self, word_embedding, word, top_n):
        print("get topn similarity word...")
        tmp = word_embedding.similar_by_word(word, top_n)
        result = {}
        for pair in tmp:
            print(pair[0], pair[1])
            result[pair[0]] = pair[1]
        print(result)
        return result

# def main():
#     utils = Utils()
#     utils.convert2bin()

def main():
    utils = Utils()
    word_embedding = utils.load_word_embedding()
    word = '我'
    top_n = 10
    utils.get_topn_similarity_word(word_embedding, word.decode('utf8'), top_n)

if __name__ == '__main__':
    main()