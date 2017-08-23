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
curdir = os.path.dirname(os.path.abspath(__file__))

from keras.callbacks import EarlyStopping, ModelCheckpoint

def update(data_loader, network):

    tk_data = data_loader.tk_data_loader()
    model_name, model = network.basic_baseline()

    previous_model_path = curdir+'/models/basic_baselineThu_Aug_17_01:40:41_2017.h5'
    if os.path.exists(previous_model_path):
        model.load_weights(previous_model_path)

    now_time = '_'.join(time.asctime(time.localtime(time.time())).split(' '))
    bst_model_path = './models/' + model_name +now_time + 'update.h5'
    print('bst_model_path:', bst_model_path)
    model_checkpoint = ModelCheckpoint(bst_model_path, save_weights_only=True)

    model.fit([tk_data[0], tk_data[1]], tk_data[2],
              batch_size=128,
              epochs=10, shuffle=True,
              callbacks=[model_checkpoint])

if __name__ == "__main__":
    data_loader = Data_Loader()
    data_loader.load_vocb()
    data_loader.stat()
    network = Network()
    network.info(data_loader)
    update(data_loader, network)
