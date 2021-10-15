#!/usr/bin/python3

import os, tensorflow as tf, numpy as np, pandas as pd
keras = tf.keras

'''
    Reads the train and test csv file of emnist-letters dataset. 
    The mapp is an array of 26 elements from A-Z_a-z representing the label of 
    each class in the csv file(26 classes).
    Returns the training and the test set. 
'''
def load_emnist_letters():
    test = pd.read_csv("../docs/emnist-letters-test.csv", delimiter= ',')
    train = pd.read_csv("../docs/emnist-letters-train.csv", delimiter= ',')

    test_data = test.iloc[:, 1:]
    test_label = np.array(test.iloc[:, 0].values)

    train_data = train.iloc[:, 1:]
    train_label = np.array(train.iloc[:, 0].values)

    train_data = np.array(train_data)
    test_data = np.array(test_data)
    
    # reshape images of emnist dataset train and set, 
    # inverts each images back to a human readable form. 
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

    # normalizing the data to get more accuracy by the prediction
    train_data /= 255.0
    test_data /= 255.0

    return (train_data, train_label), (test_data, test_label)

''' 
    Builds a deep feedforward neural network and train it on the emnist-letters training set.
    Tests the model on the test set and save the results (validation loss and validation accuracy).
'''
def train_emnist_letters():

    (train_data, train_label), (test_data, test_label) = load_emnist_letters()

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),     # input layer 

        keras.layers.Dense(512, activation='relu'),     # hidden layer 

        keras.layers.Dense(512, activation='relu'),     # hidden layer 

        keras.layers.Dense(27, activation='softmax')    # output layer 
    ])

    # compile the built deep neural network.
    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    # train network with trainings set and validates on test set
    history = model.fit(train_data, train_label, epochs=10, validation_data=(test_data, test_label))

    # give the results of the networks evaluation on the test set
    test_loss, test_acc = model.evaluate(test_data,  test_label)


    # saving the model
    save_dir = "results"
    model_name = "trained_emnist_letters"
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
    print('saved trained model at %s ', model_path)
    
    # predict each image in the test set using the built model
    prediction = model.predict(test_data)

train_emnist_letters()