import cv2
import os
from task_types import Task_type
from tensorflow import keras 
import numpy as np
import pandas as pd

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

mapp = pd.read_csv("docs/emnist-balanced-mapping.txt", delimiter= ',', header=None, squeeze=True)
digits_model = keras.models.load_model("results/trained_keras_mnist")
text_model = keras.models.load_model("results/trained_emnist")

def ocr_pre(image, type):
    if  (type == Task_type.NUMBER) :  
        num = digits_model.predict(image)
        labels = [i for i in range(10)]
        result = labels[np.argmax(num)]

    elif (type == Task_type.TEXT or type == Task_type.TEXT_NO_NUMBERS) :
        text = text_model.predict(image)
        index = np.argmax(text)
        result = chr(mapp[index])

    else:
        raise ValueError("type not valid! TYPE: [2] for numbers, [3] for text with numbers, [4] for text without numbers")
       

    return result

