import io

import cv2 as cv
import numpy as np
from PIL import Image

from Document import Document
from Task import Task
from task_types import Task_type
from checkboxchecker import find_checkboxes
from letterdetection import lettercropping
from Exam import Exam
from PIL import Image
Image.MAX_IMAGE_PIXELS = None


def autocorrect_exams(document: Document) -> Document:
    for exam in document.exams:
        image = cv.cvtColor(np.array(exam.img), cv.COLOR_RGB2BGR)
        task: Task

        for task in exam.tasks:
            task_type = task.task_type
            roi = [task.x,task.y,task.x+task.width,task.y+task.height]

            if task_type == Task_type.SINGLE_CHOICE:
                task.actual_answer, img = find_checkboxes(image, roi)
                exam.img_modified.paste(img, (task.x, task.y))

            elif task_type == Task_type.MULTIPLE_CHOICE:
                task.actual_answer, img = find_checkboxes(image, roi)
                exam.img_modified.paste(img, (task.x, task.y))

            elif task_type == Task_type.NUMBER:
                task.actual_answer = lettercropping(image, roi, task_type)

            elif task_type == Task_type.TEXT:
                task.actual_answer = lettercropping(image, roi, task_type)

            elif task_type == Task_type.TEXT_NO_NUMBERS:
                task.actual_answer = lettercropping(image, roi, task_type)

            elif task_type == Task_type.SHAPE:
                pass

            else:
                raise ValueError("Unknown Task Type")

    return document


def autodetect_expected_answers(document: Document):
    image = cv.cvtColor(np.array(document.img), cv.COLOR_RGB2BGR)

    for task in document.tasks:
        task_type = task.task_type
        roi = [task.x,task.y,task.x+task.width,task.y+task.height]

        if task_type == Task_type.SINGLE_CHOICE:
            task.expected_answer, img = find_checkboxes(image, roi)
            document.img_modified.paste(img, (task.x, task.y))

        elif task_type == Task_type.MULTIPLE_CHOICE:
            task.expected_answer, img = find_checkboxes(image, roi)
            document.img_modified.paste(img, (task.x, task.y))

        elif task_type == Task_type.NUMBER:
            task.expected_answer = lettercropping(image, roi, task_type)

        elif task_type == Task_type.TEXT:
            task.expected_answer = lettercropping(image, roi, task_type)

        elif task_type == Task_type.TEXT_NO_NUMBERS:
            task.expected_answer = lettercropping(image, roi, task_type)

        elif task_type == Task_type.SHAPE:
            pass

        else:
            raise ValueError("Unknown Task Type")

    return document
