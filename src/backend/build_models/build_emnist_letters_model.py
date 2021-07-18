#!/usr/bin/python3

import os

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
keras = tf.keras

#mapp = pd.read_csv("docs/emnist-balanced-mapping.txt", delimiter= ',', header=None, squeeze=True)

def load_nist():
    test = pd.read_csv("docs/emnist-letters-test.csv", delimiter= ',')
    train = pd.read_csv("docs/emnist-letters-train.csv", delimiter= ',')

    test_data = test.iloc[:, 1:]
    test_label = np.array(test.iloc[:, 0].values)

    train_data = train.iloc[:, 1:]
    train_label = np.array(train.iloc[:, 0].values)
    print(train_data.shape,train_label.shape,test_data.shape,test_label.shape)
    print('\n')
    train_data = np.array(train_data)
    test_data = np.array(test_data)

    #reshape images of emnist dataset train and set(building the input vector from 28x28)
    train_data = train_data.reshape(88799, 28, 28)
    train_data = [np.fliplr(image) for image in train_data] 
    train_data = [np.rot90(image) for image in train_data]
    train_data = np.asarray(train_data)

    test_data = test_data.reshape(14799, 28, 28)
    test_data = [np.fliplr(image) for image in test_data]
    test_data = [np.rot90(image) for image in test_data]
    test_data = np.asarray(test_data)

    train_data = train_data.astype('float32')
    test_data = test_data.astype('float32')
    print(train_data.shape,train_label.shape,test_data.shape,test_label.shape)
    print('\n')
    # normalizing the data to help with the training
    train_data /= 255.0
    test_data /= 255.0

    return (train_data, train_label), (test_data, test_label)

def train_emnist():

    (train_data, train_label), (test_data, test_label) = load_nist()
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),  # input layer (1)
        keras.layers.Dense(128, activation='relu'),  # hidden layer (2)
        keras.layers.Dense(512, activation='relu'),  # hidden layer (2)
        keras.layers.Dense(27, activation='softmax') # output layer (3)
    ])

    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    model.fit(train_data, train_label, epochs=10)

    test_loss, test_acc = model.evaluate(test_data,  test_label)

    print('Test accuracy:', test_acc)

    #saving the model
    save_dir = "results"
    model_name = "trained_emnist_letters"
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
    print('saved trained model at %s ', model_path)

    prediction = model.predict(test_data)
    mapp = [i for i in range (97, 122+1)]
    plt.figure(figsize = (10,10))
    row, colums = 4, 4
    for i in range(16):
        plt.subplot(colums, row, i + 1)
        index = randint(0, len(test_data))
        plt.imshow(test_data[index], cmap='Greys')
        plt.title(f"pre={chr(mapp[np.argmax(prediction[index])])} real={chr(mapp[test_label[index]])}")
        plt.axis('off')
    plt.savefig("demo_nist.png", bbox_inches='tight')
    plt.show()

train_emnist()
