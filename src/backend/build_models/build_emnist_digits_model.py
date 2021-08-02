#!/usr/bin/python3

import tensorflow as tf, pandas as pd
from build_cnn_models import train_emnist
keras = tf.keras

'''
    Reads the train and test csv file of emnist-digits dataset. 
    The mapp is an array of 10 elements from 0 to 9 representing the label of each class 
    in both csv files(trainings and test set).
    Returns the training, the test set and the mapp.
'''
def load_emnist_digits():
    test = pd.read_csv("../docs/emnist-digits-test.csv", delimiter= ',')
    train = pd.read_csv("../docs/emnist-digits-train.csv", delimiter= ',')
    mapp = list(range(10))
    return train, test, mapp

train, test, mapp = load_emnist_digits()

train_emnist(512, 10, train, test, mapp, "digits")


