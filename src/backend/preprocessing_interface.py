import cv2 as cv
import numpy as np
from PIL import Image

from Document import Document
from Task import Task
from task_types import Task_type
from checkboxchecker import find_checkboxes
from letterdetection import lettercropping

def preprocessing_interface(document: Document):
    image = cv.cvtColor(np.array(document.img), cv.COLOR_RGB2BGR)
    tasks = document.tasks
    processed_image = image.copy()
    roi = []
    for task in tasks:
        task_type = task.task_type
        roi = task.x,task.y,task.x+task.width,task.y+task.height

        if task_type == Task_type.SINGLE_CHOICE:
            find_checkboxes(image, roi)
        elif task_type == Task_type.MULTIPLE_CHOICE:
            find_checkboxes(image, roi)
        elif task_type == Task_type.NUMBER:
            lettercropping(image, roi, task_type)
        elif task_type == Task_type.TEXT:
            lettercropping(image, roi, task_type)
        elif task_type == Task_type.TEXT_NO_NUMBERS:
            lettercropping(image, roi, task_type)
        elif task_type == Task_type.SHAPE:
            pass
        else:
            raise ValueError("Unknown Task Type")
            
            
    
    return document
