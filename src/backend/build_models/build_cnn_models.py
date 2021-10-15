#!/usr/bin/python3
from random import randint
import os, tensorflow as tf, numpy as np, matplotlib.pyplot as plt
keras = tf.keras

''' 
    Extracts respectively the test and the train dataset from the emnist csv file. 
    The Labels of both sets are extracted at the first(0) column of each emnist class.
    The image datas of the both sets are extracted from the second(1) to the last column 
    of each emnist class. Both sets are transformed as arrays to make datas reshaping possible.
    Returns extracted datas and labels of the train and test set respectively. 
'''
def extract_datas(test, train): 
    test_data = test.iloc[:, 1:]
    test_label = np.array(test.iloc[:, 0].values)

    train_data = train.iloc[:, 1:]
    train_label = np.array(train.iloc[:, 0].values)

    train_data = np.array(train_data)
    test_data = np.array(test_data)

    return (train_data, train_label), (test_data, test_label)

'''
    Reshapes each image array, reverses the image horizontaly from the left to the right, and rotate it 
    back by 90 grad anticlockwise to make it human readable.
    Downscales the image pixels to avoid big values by the prediction and get a better accuracy.  
    Converts each image array to a numpy array and change type from uint8 to float32 to allow normalization.
    Normalizes the datas by scaling the pixel intensities of the images from [0, 255] down to [0, 1].
'''
def image_preprocessing(train_data, test_data):

    train_data = [data.reshape(28, 28, 1) for data in train_data] 
    train_data = [np.fliplr(image) for image in train_data] 
    train_data = [np.rot90(image) for image in train_data] 
    train_data = np.asarray(train_data) 

    test_data = [data.reshape(28, 28, 1) for data in test_data]
    test_data = [np.fliplr(data) for data in test_data] 
    test_data = [np.rot90(data) for data in test_data]
    test_data = np.asarray(test_data)

    train_data = train_data.astype('float32')
    test_data = test_data.astype('float32')

    train_data /= 255.0
    test_data /= 255.0

    return train_data, test_data

''' plots some sample images. '''
def plot_sample_images(data, label, mapp, prediction, data_name):
    plt.figure(figsize = (10,10))
    row, colums = 4, 4
    for i in range(16):
        plt.subplot(colums, row, i + 1)
        index = randint(0, len(data))
        plt.imshow(tf.squeeze(data[index]), cmap='Greys')
        plt.title(f"pre={chr(mapp[np.argmax(prediction[index])])} real={chr(mapp[label[index]])}")
        plt.axis('off')
    plt.savefig(f"emnist_{data_name}_plot.png", bbox_inches='tight')
    plt.show()

''' Plots graphs to show the metrics based on the trainings result done on the train and validations set. '''
def plot_metrics(history, data, label, model):
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='lower right')
    plt.show()

    plt.subplot(2,1,2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss']) 
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')  
    plt.show()

    plt.tight_layout()
    test_loss, test_acc = model.evaluate(data,  label, verbose=2)
    print(test_acc, test_loss)


''' 
    Builds a 2 dimensional Convolutional Neural Network, trains the network 
    on the trainings set and validates it on the test set. 
'''
def train_emnist(num_nodes, num_classes, train, test, mapp, data_name):   
    (train_data, train_label), (test_data, test_label) = extract_datas(train, test)
    train_data, test_data = image_preprocessing(train_data, test_data)

    model = keras.Sequential([
        keras.layers.Conv2D(32, (5, 5), activation='relu', input_shape= (28, 28, 1)), 
        keras.layers.MaxPooling2D(2,2),
        keras.layers.BatchNormalization(), 
        keras.layers.Conv2D(32, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2,2), 
        keras.layers.BatchNormalization(),
        keras.layers.Flatten(),
        keras.layers.Dense(num_nodes, activation='relu'), 
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(num_classes, activation='softmax')
    ])

    #compile the built 2D CNN neural network
    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    # train network with trainings set and validates on test set
    history = model.fit(train_data, train_label, epochs=10, validation_data=(test_data, test_label))

    #saving the model
    save_dir = "results"
    model_name = f"trained_emnist {data_name}"
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
    print('saved trained model at %s ', model_path)

    prediction = model.predict(test_data)

    # call functions plot_metrics() or plot sample_images() to see the predictions and the trainimgs results on train and test set.
