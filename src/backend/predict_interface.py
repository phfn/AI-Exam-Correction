import cv2 as cv, os, math
from task_types import Task_type
from tensorflow import keras 
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract as pyt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

mapp = pd.read_csv("docs/emnist-balanced-mapping.txt", delimiter= ',', header=None, squeeze=True)
letters_mapp = [l for l in range(97, 122+1)]
digits_model = keras.models.load_model("results/trained_mnist_dnn_model")
digits_model_mnist = keras.models.load_model("results/trained_keras_mnist")
byMerge_model = keras.models.load_model("results/trained_emnist_dnn")
balanced_model = keras.models.load_model("results/trained_emnist")
letters_model = keras.models.load_model("results/trained_emnist_letters")
err_msg = "type not valid! TYPE: [2] for numbers, [3] for text with numbers, [4] for text without numbers"

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
    colsPadding = (int(math.ceil((28 - cols) / 2.0)), int(math.floor((28 - cols) / 2.0)))
    rowsPadding = (int(math.ceil((28 - rows) / 2.0)), int(math.floor((28 - rows) / 2.0)))
    image = np.lib.pad(image, (rowsPadding, colsPadding), 'constant')
    padded = image.reshape(-1,28,28)
    padded = padded.astype(np.float32)

    return padded

def ocr_pre(image, type):
    if  (type == Task_type.NUMBER) :  
        list_emnist_digits = digits_model.predict(image)
        list_mnist = digits_model_mnist.predict(image)
        pre_rate_emnist = max(list_emnist_digits)
        pre_rate_mnist = max(list_mnist)
        labels = [i for i in range(10)]
        if (pre_rate_emnist > pre_rate_mnist).any():
            result = labels[np.argmax(list_emnist_digits)]
        else:
            result = labels[np.argmax(list_mnist)]

    elif (type == Task_type.TEXT_NO_NUMBERS) :
        prediction_byMerge_model = byMerge_model.predict(image)
        prediction_balanced_model = balanced_model.predict(image)
        prediction_letters_model = letters_model.predict(image)
        index1 = np.argmax(prediction_byMerge_model)
        index2 = np.argmax(prediction_balanced_model)
        index3 = np.argmax(prediction_letters_model)
        pre_rate_byMerge = max(prediction_byMerge_model)
        pre_rate_balanced = max(prediction_balanced_model)
        pre_rate_letters = max(prediction_letters_model)
        index = index3-1
         
        if (max(pre_rate_byMerge) > max(pre_rate_balanced)).any():
            if (max(pre_rate_byMerge) > max(pre_rate_letters)).any():
                result = chr(mapp[index1])
            else:
                result = chr(letters_mapp[index])
        else:
            if (max(pre_rate_balanced) > max(pre_rate_letters)).any():
                result = chr(mapp[index2])
            else:
                result = chr(letters_mapp[index])
    
    elif (type == Task_type.TEXT):
        prediction_balanced_model = balanced_model.predict(image)
        index3 = np.argmax(prediction_balanced_model)
        result = chr(mapp[index3])
    else:
        raise ValueError(err_msg)

    return result

def pre_ocr_with_tesseract(image, type):

    if(type == Task_type.TEXT_NO_NUMBERS):
        img = Image.fromarray(image)
        config = r'-l deu_ocr+deu --oem 2 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8'
        result = pyt.image_to_string(img, config=config)
        result = os.linesep.join([s for s in result.splitlines() if s])

    else:
        raise ValueError(err_msg)
       
    return result
