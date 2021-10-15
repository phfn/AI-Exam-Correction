#!/usr/bin/python3

import tensorflow as tf, pandas as pd
from build_cnn_models import train_emnist
keras = tf.keras

''' 
    Reads the train and test csv file of emnist-balanced dataset. 
    The mapping text file is also read and contains the label each class of a dataset.
    Returns the training, the test set and the mapp.     
'''
def load_emnist_balanced():
    mapp = pd.read_csv("../docs/emnist-balanced-mapping.txt", delimiter= ',', header=None, squeeze=True)
    test = pd.read_csv("../docs/emnist-balanced-test.csv", delimiter= ',')
    train = pd.read_csv("../docs/emnist-balanced-train.csv", delimiter= ',')
    return train, test, mapp

train, test, mapp = load_emnist_balanced()

train_emnist(512, 47, train, test, mapp, "balanced")