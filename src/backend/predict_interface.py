import os
import math
import cv2 as cv
from tensorflow import keras 
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract as pyt
from task_types import Task_type


digits_mapp = list(range(10))
emnist_letters_mapp = list(range(97, 122+1))
mapp = pd.read_csv("docs/emnist-balanced-mapping.txt", delimiter= ',', header=None, squeeze=True)
digits_model = keras.models.load_model("results/trained_emnist_digits")
digits_model_mnist = keras.models.load_model("results/trained_keras_mnist")
by_merge_model = keras.models.load_model("results/trained_emnist_bymerge")
balanced_model = keras.models.load_model("results/trained_emnist_balanced")
letters_model = keras.models.load_model("results/trained_emnist_letters")
ERR_MSG = "type not valid! TYPE: [2] for numbers, [3] for text with numbers, [4] for text without numbers"

'''
    reshape the image array size to 28x28 by filling its edges with zeros, according
    to the number of times zeros should be added before the first element and 
    after the last element of each axis of the image array.
'''
def enlarge_image(image):
    rows, cols = image.shape
    if rows > cols:
        factor = 20.0 / rows
        rows = 20
        cols = int(round(cols * factor))
        image = cv.resize(image, (cols, rows))
    else:
        factor = 20.0 / cols
        cols = 20
        rows = int(round(rows * factor))
        image = cv.resize(image, (cols, rows), interpolation=cv.INTER_CUBIC)
    cols_padding = (int(math.ceil((28 - cols) / 2.0)), int(math.floor((28 - cols) / 2.0)))
    rows_padding = (int(math.ceil((28 - rows) / 2.0)), int(math.floor((28 - rows) / 2.0)))
    image = np.lib.pad(image, (rows_padding, cols_padding), 'constant')
    padded = image.reshape(-1,28,28)
    padded = padded.astype(np.float32)

    return padded

'''
    Reshapes the image before using a model based on a 2D convolutional neural network.
    Changes the type of reshaped image arrays to allow normalisation (downscaling of 
    pixels to the interval [0 1]).
    Normalisation is very important to achieve higher accuracy in prediction.
'''
def reshape_image_for_cnn_prediction(image):
    image = image.reshape(-1, 28, 28, 1)
    image = image.astype(np.float32)
    image = image/255.0 
    
    return image

'''
    Predicts the image with each of the model corresponding to the task type 
    specified as parameter.
    Compares the prediction rate of each of these models with the other.
    Returns the result of the model with the highest prediction rate.
    The index of the mapp is equivalent to the index of the prediction array 
    having the highest prediction rate.  
    By the type : TEXT_NO_NUMBERS there is just one model available, therefore 
    no comparison will be performed.  
    When no type selected a valueerror is thrown.
'''
def ocr_pre(image, type):
    if(type == Task_type.NUMBER):  

        list_mnist = digits_model_mnist.predict(image)
        image = reshape_image_for_cnn_prediction(image)
        list_emnist_digits = digits_model.predict(image)

        pre_rate_emnist = max(list_emnist_digits)
        pre_rate_mnist = max(list_mnist)
       
        if(pre_rate_emnist > pre_rate_mnist).any():
            result = digits_mapp[np.argmax(list_emnist_digits)]

        else:
            result = digits_mapp[np.argmax(list_mnist)]

    elif(type == Task_type.TEXT):

        image = reshape_image_for_cnn_prediction(image)
        prediction_by_merge_model = by_merge_model.predict(image)
        prediction_balanced_model = balanced_model.predict(image)

        index1 = np.argmax(prediction_by_merge_model)
        index2 = np.argmax(prediction_balanced_model)

        pre_rate_by_merge = np.amax(prediction_by_merge_model)
        pre_rate_balanced = np.amax(prediction_balanced_model)


        if(pre_rate_by_merge > pre_rate_balanced):
            result = chr(mapp[index1])

        else:
            result = chr(mapp[index2])

    elif(type == Task_type.TEXT_NO_NUMBERS):                       
        prediction_letters_model = letters_model.predict(image)
        index3 = np.argmax(prediction_letters_model)
        index = index3-1
        result = chr(emnist_letters_mapp[index])
            
    else:
        raise ValueError(ERR_MSG)

    return result

'''
    Uses traineddata files built using tesseract-ocr engine to predict images as block of text.
    Predicts only normal letters and diacritical letters (lower- and uppercase).
    Converts the output to string and returns it.
    Use a special function "os.linesep,join()" to remove empty lines from the output. 
    When no type selected a Valueerror is thrown.
'''
def pre_ocr_with_tesseract(image, type):

    if(type == Task_type.TEXT_NO_NUMBERS):
        img = Image.fromarray(image)
        config = r'-l ger_ocr --oem 2 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 6'
        result = pyt.image_to_string(img, config=config)
        result = os.linesep.join([s for s in result.splitlines() if s])

    else:
        raise ValueError(ERR_MSG)

    return result
