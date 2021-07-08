import cv2 as cv
import numpy as np
from PIL import Image

from Exam_container import Exam_container
from task_types import Task_type
from checkboxchecker import find_checkboxes
from letterdetection import lettercropping
from PIL import Image
Image.MAX_IMAGE_PIXELS = None


def autocorrect_exams(exam_container: Exam_container) -> Exam_container:
    for exam in exam_container.student_exams:
        image = cv.cvtColor(np.array(exam.image), cv.COLOR_RGB2BGR)

        for task in exam.tasks:
            roi = [task.x,task.y,task.x+task.width,task.y+task.height]

            if task.type == Task_type.SINGLE_CHOICE:
                task.actual_answer, img = find_checkboxes(image, roi)
                exam.img_modified.paste(img, (task.x, task.y))

            elif task.type == Task_type.MULTIPLE_CHOICE:
                task.actual_answer, img = find_checkboxes(image, roi)
                exam.img_modified.paste(img, (task.x, task.y))

            elif task.type == Task_type.NUMBER:
                task.actual_answer = lettercropping(image, roi, task.type)

            elif task.type == Task_type.TEXT:
                task.actual_answer = lettercropping(image, roi, task.type)

            elif task.type == Task_type.TEXT_NO_NUMBERS:
                task.actual_answer = lettercropping(image, roi, task.type)

            elif task.type == Task_type.SHAPE:
                pass

            else:
                raise ValueError("Unknown Task Type")

    return exam_container


def autodetect_expected_answers(exam_container: Exam_container):
    image = cv.cvtColor(np.array(exam_container.correct_exam.image), cv.COLOR_RGB2BGR)

    for task in exam_container.correct_exam.tasks:
        task_type = task.type
        roi = [task.x,task.y,task.x+task.width,task.y+task.height]

        if task_type == Task_type.SINGLE_CHOICE:
            task.expected_answer, img = find_checkboxes(image, roi)
            exam_container.correct_exam.image_modified.paste(img, (task.x, task.y))

        elif task_type == Task_type.MULTIPLE_CHOICE:
            task.expected_answer, img = find_checkboxes(image, roi)
            exam_container.correct_exam.image_modified.paste(img, (task.x, task.y))

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

    return exam_container
