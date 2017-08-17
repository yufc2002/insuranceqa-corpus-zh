#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 Guoxiu He. All Rights Reserved"
__author__ = "Guoxiu He"
__date__ = "2017-08-08:18:32:05"

from data_loader import Data_Loader
from model import Network

import time
import os

from keras.callbacks import EarlyStopping, ModelCheckpoint

def train(data_loader, network):

    train, valid, test = data_loader.process()
    model_name, model = network.basic_baseline()

    now_time = '_'.join(time.asctime(time.localtime(time.time())).split(' '))
    bst_model_path = './models/' + model_name +now_time + '.h5'
    print('bst_model_path:', bst_model_path)
    early_stopping = EarlyStopping(monitor='val_acc', patience=3)
    model_checkpoint = ModelCheckpoint(bst_model_path, monitor='val_acc', save_best_only=True, save_weights_only=True)

    model.fit([train[0], train[1]], train[2],
              batch_size=128,
              epochs=100, shuffle=True,
              validation_data=([valid[0], valid[1]], valid[2]),
              # callbacks=[model_checkpoint])
              callbacks=[early_stopping, model_checkpoint])

    if os.path.exists(bst_model_path):
        model.load_weights(bst_model_path)

    print('test:', model.evaluate([test[0], test[1]], test[2], batch_size=128))

if __name__ == "__main__":
    data_loader = Data_Loader()
    data_loader.load()
    data_loader.stat()
    network = Network()
    network.info(data_loader)
    train(data_loader, network)
