#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 Guoxiu He. All Rights Reserved"
__author__ = "Guoxiu He"
__date__ = "2017-08-08:18:32:05"

from data_loader import Data_Loader

from keras.models import Model, Sequential
from keras.layers import Dense, Embedding, LSTM, GRU, Conv1D, Conv2D, GlobalMaxPooling1D, GlobalAveragePooling1D
from keras.layers import Dropout, Input, Activation, Flatten
from keras.layers import TimeDistributed, RepeatVector, Permute, Lambda, Bidirectional, Merge
from keras.layers.merge import concatenate, add, dot, multiply
from keras.optimizers import RMSprop, Adam, SGD, Adagrad, Adadelta, Adamax, Nadam
from keras.layers.advanced_activations import PReLU
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K

class Network(object):
    def __init__(self, embedding_dim=200, num_rnn=200, num_dense=200,
                 rate_dropout_rnn=0.5, rate_dropout_dense=0.5, act='relu'):
        print("Building the Network...")
        self.embedding_dim = embedding_dim
        self.num_rnn = num_rnn
        self.num_dense = num_dense
        self.rate_dropout_rnn = rate_dropout_rnn
        self.rate_dropout_dense = rate_dropout_dense
        self.act = act

    def info(self, data_loader):
        self.nb_words = data_loader.vocab_size + 1
        self.question_length = data_loader.max_len_train_question
        self.utterance_length = data_loader.max_len_train_utterance

    def basic_baseline(self):
        embedding_question = Embedding(input_dim=self.nb_words,
                                       output_dim=self.embedding_dim,
                                       input_length=self.question_length,
                                       embeddings_initializer='random_uniform')

        embedding_utterance = Embedding(input_dim=self.nb_words,
                                        output_dim=self.embedding_dim,
                                        input_length=self.utterance_length,
                                        embeddings_initializer='random_uniform')

        rnn_question = Bidirectional(GRU(units=self.num_rnn,
                                         dropout=self.rate_dropout_rnn,
                                         recurrent_dropout=self.rate_dropout_rnn))

        rnn_utterance = Bidirectional(GRU(units=self.num_rnn,
                                          dropout=self.rate_dropout_rnn,
                                          recurrent_dropout=self.rate_dropout_rnn))

        sequence_question = Input(shape=(self.question_length,), dtype='int32')
        embedded_sequences_question = embedding_question(sequence_question)

        sequence_utterance = Input(shape=(self.utterance_length,), dtype='int32')
        embedded_sequences_utterance = embedding_utterance(sequence_utterance)

        question = rnn_question(embedded_sequences_question)

        utterance = rnn_utterance(embedded_sequences_utterance)

        merged = concatenate([question, utterance])
        merged = Dropout(self.rate_dropout_dense)(merged)
        merged = BatchNormalization()(merged)

        merged = Dense(self.num_dense, activation=self.act)(merged)
        merged = Dropout(self.rate_dropout_dense)(merged)
        merged = BatchNormalization()(merged)

        preds = Dense(2, activation='softmax')(merged)

        ########################################
        ## train the model
        ########################################
        model = Model(inputs=[sequence_question, sequence_utterance], outputs=preds)
        model.compile(loss='categorical_crossentropy',
                      optimizer='nadam',
                      metrics=['acc'])
        model.summary()
        # print(STAMP)
        return 'basic_baseline', model

def main():
    model = Network()
    data_loader = Data_Loader()
    data_loader.stat()
    model.info(data_loader)
    model_name, basic_baseline = model.basic_baseline()
    print(model_name)

if __name__ == '__main__':
    main()
