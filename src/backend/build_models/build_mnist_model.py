#!/usr/bin/python3

import os, tensorflow as tf
keras = tf.keras

''' 
    Loads mnist train and test dataset from the keras.datasets library.
    The mapp is an array of 10 elements representing the label of each class(0 to 9).
    Returns each tuple of trainings an test set.
'''
def load_mnist():

    (train_data, train_label), (test_data, test_label) = keras.datasets.mnist.load_data()

    #change array type from uint8 to float32 to allow normalization
    train_data = train_data.astype('float32')
    test_data = test_data.astype('float32')

    mapp = list(range(10))

    # normalize the datas by scaling the pixel intensities 
    # of the images from [0, 255] down to [0, 1]
    train_data /= 255.0
    test_data /= 255.0

    return (train_data, train_label), (test_data, test_label), mapp

''' 
    Builds a deep neural network with 2 hidden layers and train it on the mnist training set.
    validates the model on the test set and save the results(validation loss and validation accuracy).
'''
def train_mnist():

    (train_data, train_label), (test_data, test_label), mapp = load_mnist()

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),     # input layer

        keras.layers.Dense(512, activation="relu"),     # hidden layer

        keras.layers.Dense(512, activation="relu"),     # hidden layer

        keras.layers.Dense(10,  activation="softmax")   # output layer
    ])

    #compile the built deep neural network.
    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    # train network with trainings set and validates on test set
    history = model.fit(train_data, train_label, epochs=10, validation_data=(test_data, test_label))

    # give the results of the network evaluation on the test set
    test_loss, test_acc = model.evaluate(test_data,  test_label)

    #saving the model
    save_dir = "results"
    model_name = "trained_mnist"
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
    print('saved trained model at %s ', model_path)

    # predict each image in the test set using the built model
    prediction = model.predict(test_data)


train_mnist()