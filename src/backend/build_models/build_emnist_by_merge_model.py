#!/usr/bin/python3

import tensorflow as tf, pandas as pd
from build_cnn_models import train_emnist
keras = tf.keras

'''
    Reads the train and test csv file of emnist by_merge dataset. 
    The mapping text file is also read and represents the label for each class in the csv file.
    This mapp is from the emnist balanced dataset(the emnist balanced and by_merge dataset have both 47 classes).
    Returns the training, the tests set and the mapp.
''' 
def load_emnist_by_merge():
    mapp = pd.read_csv("../docs/emnist-balanced-mapping.txt", delimiter= ',', header=None, squeeze=True)
    test = pd.read_csv("../docs/emnist-bymerge-test.csv", delimiter= ',')
    train = pd.read_csv("../docs/emnist-bymerge-train.csv", delimiter= ',')
    return train, test, mapp

train, test, mapp = load_emnist_by_merge()

train_emnist(512, 47, train, test, mapp, "by_merge")