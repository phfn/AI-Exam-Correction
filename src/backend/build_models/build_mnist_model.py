#!/usr/bin/python3

import os

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
#import pandas as pd
from random import randint
import matplotlib.pyplot as plt
keras = tf.keras
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils


(train_data, train_label), (test_data, test_label) = keras.datasets.mnist.load_data()

#reshape images of mnist dataset train and set(building the input vector from 28x28)
train_data = train_data.reshape(60000, 28, 28)
test_data = test_data.reshape(10000, 28, 28)
train_data = train_data.astype('float32')
test_data = test_data.astype('float32')

# Scale pixel intensities of the images from [0, 255] down to [0, 1]
train_data /= 255.0
test_data /= 255.0

#building a linear stack of layers (with add() function) with the sequetial model
model = Sequential()
model.add(Flatten(input_shape=(28, 28)))  #input layer

model.add(Dense(512))                     # hidden layer
model.add(Activation('relu')) 

model.add(Dense(512))                     # hidden layer
model.add(Activation('relu'))  

model.add(Dense(10))                      # output layer
model.add(Activation('softmax'))  

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_data, train_label, epochs=10, validation_data=(test_data, test_label))

#saving the model
save_dir = "results"
model_name = "trained_keras_mnist"
model_path = os.path.join(save_dir, model_name)
model.save(model_path)
print('saved trained model at %s ', model_path)

#plotting the metrics
fig = plt.figure()
plt.subplot(2,1,1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='lower right')

plt.subplot(2,1,2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')  

plt.tight_layout()
plt.savefig('metrics')


loss_and_metrics = model.evaluate(test_data, test_label, verbose=2)

print("test loss", loss_and_metrics[0])
print("test accuracy", loss_and_metrics[1])

labels = [i for i in range(10)]

prediction = model.predict(test_data)
row = 5
colums = 6
labels = [i for i in range(10)]
for i in range(30):  
    plt.subplot(colums, row, i + 1)
    index = randint(0, len(test_data))
    plt.imshow(test_data[index], cmap='gray_r')
    plt.title(f"pre={labels[np.argmax(prediction[index])]} real={labels[test_label[index]]}")
    plt.axis('off')
plt.show()
#fig.savefig('demo.png', bbox_inches='tight')
