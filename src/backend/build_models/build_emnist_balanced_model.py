#!/usr/bin/python3

import os

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
from tensorflow.python.keras.layers.core import Dropout
keras = tf.keras

""" loads each data from emnist dataset. The csv mapp file for future predictions is also read. """
def load_emnist():
    mapp = pd.read_csv("docs/emnist-balanced-mapping.txt", delimiter= ',', header=None, squeeze=True)
    test = pd.read_csv("docs/emnist-balanced-test.csv", delimiter= ',')
    train = pd.read_csv("docs/emnist-balanced-train.csv", delimiter= ',')
    return test, train, mapp

""" 
    extracts respectively the test and the train datas from the emnist csv file. 
    The Labels of both sets are extracted from the first column of the emnist csv file.
    The proper datas of the both sets are extracted from the first to the last column of the emnist csv file.
    both sets are transformed as arrays to make future datas reshaping possible.
    returns extracted datas and labels of the train and test set respectively. 
"""
def extract_datas(test, train): 
    test_data = test.iloc[:, 1:]
    test_label = np.array(test.iloc[:, 0].values)

    train_data = train.iloc[:, 1:]
    train_label = np.array(train.iloc[:, 0].values)

    print(train_data.shape,train_label.shape,test_data.shape,test_label.shape)
    print('\n')

    train_data = np.array(train_data)
    test_data = np.array(test_data)

    return (train_data, train_label), (test_data, test_label)

""" reshapes each data array and downscales the images pixels for a better training with CNN. """
def image_preprocessing(train_data, test_data):
    #reshape each image of train and test set
    train_data = [data.reshape(28, 28) for data in train_data]
    train_data = [np.fliplr(image) for image in train_data]
    train_data = [np.rot90(image) for image in train_data]
    train_data = np.asarray(train_data)

    test_data = [data.reshape(28, 28) for data in test_data]
    test_data = [np.fliplr(data) for data in test_data]
    test_data = [np.rot90(data) for data in test_data]
    test_data = np.asarray(test_data)

    train_data = train_data.astype('float32')
    test_data = test_data.astype('float32')

    # downscale image pixels from [0, 255] to [0, 1]
    train_data /= 255.0
    test_data /= 255.0

    print(train_data.shape, test_data.shape)
    return train_data, test_data

""" plots some sample images. """
def plot_sample_images(data, label, mapp):
    plt.figure(figsize = (10,10))
    row, colums = 4, 4
    for i in range(16):
        plt.subplot(colums, row, i+1)
        index = randint(0, len(data))
        plt.savefig("plot_pics/emnist_plot")
        print(data[index].shape)
        plt.imshow(tf.squeeze(data[index]), cmap='gray_r')
        print(label[index])
        num = int(label[index])
        print(num)
        plt.title(chr(mapp[num]))
    plt.show()


""" builds and train the CNN Network to get a performant model for future predictions. """
def train_emnist():
    train, test, mapp = load_emnist()
    (train_data, train_label), (test_data, test_label) = extract_datas(train, test)
    train_data, test_data = image_preprocessing(train_data, test_data)
    plot_sample_images(train_data, train_label, mapp)

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28, 1)),  # input layer (1)
        keras.layers.Dense(128, activation='relu'),  # hidden layer (2)
        keras.layers.Dense(512, activation='relu'),  # hidden layer (2)
        keras.layers.Dense(47, activation='softmax') # output layer (3)
    ])

    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    model.fit(train_data, train_label, epochs=10)

    test_loss, test_acc = model.evaluate(test_data,  test_label)

    print('Test accuracy:', test_acc)

    #saving the model
    save_dir = "results"
    model_name = "trained_emnist"
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
    print('saved trained model at %s ', model_path)

    prediction = model.predict(test_data)

    plt.figure(figsize = (10,10))
    row, colums = 4, 4
    for i in range(16):
        plt.subplot(colums, row, i + 1)
        index = randint(0, len(test_data))
        plt.imshow(tf.squeeze(test_data[index]), cmap='Greys')
        plt.title(f"pre={chr(mapp[np.argmax(prediction[index])])} real={chr(mapp[test_label[index]])}")
        plt.axis('off')
    plt.savefig("demo_emnist.png", bbox_inches='tight')
    plt.show()

train_emnist()
