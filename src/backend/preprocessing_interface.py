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

    try:
        validate_exam_container(exam_container, True)
    except Exception as e:
        raise e

    for exam in exam_container.student_exams:
        image = cv.cvtColor(np.array(exam.image), cv.COLOR_RGB2BGR)

        for task in exam.tasks:
            roi = [task.x,task.y,task.x+task.width,task.y+task.height]

            if task.type == Task_type.SINGLE_CHOICE:
                task.actual_answer, img = find_checkboxes(image, roi)
                exam.image_modified.paste(img, (task.x, task.y))

            elif task.type == Task_type.MULTIPLE_CHOICE:
                task.actual_answer, img = find_checkboxes(image, roi)
                exam.image_modified.paste(img, (task.x, task.y))

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

    try:
        validate_exam_container(exam_container, False)
    except Exception as e:
        raise e

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


def validate_exam_container(exam_container: Exam_container, check_student_exams : bool):

    if exam_container.correct_exam.image.width <= 27 or exam_container.correct_exam.image.height <= 27:
        raise FileNotFoundError("Incorrect image size, has to be at least 28x28 pixel")

    for index, task in enumerate(exam_container.correct_exam.tasks):
        if task.x < 0 or task.y < 0:
            raise ValueError("Task ", str(index), " has negativ coordinates.")

        if task.width <= 27 or task.height <= 27:
            raise ValueError("Task ", str(index), " has negativ dimensions.")

        if task.max_points < 0:
            raise ValueError("Task ", str(index), " has a negativ of maximum points")

        if task.deduction_per_error < 0:
            raise ValueError("In task ", str(index), " deduction_per_error should be positiv (or zero)")


    if check_student_exams:
        for exam_num, exam in enumerate(exam_container.student_exams):

            if exam.image.width <= 27 or exam.image.height <= 27:
                raise FileNotFoundError("Student exam #", exam_num, " image too small (needs at least 28x28)")
            
            # Check every exam task
            for task_num, task in enumerate(exam.tasks):
                
                if task.x < 0 or task.y < 0:
                    raise ValueError("Task ", str(task_num), " in exam #", str(exam_num), " has negativ coordinates.")

                if task.width <= 0 or task.height <= 0:
                    raise ValueError("Task ", str(task_num), " in exam #", str(exam_num), " has negativ dimensions.")

                if task.max_points < 0:
                    raise ValueError("Task ", str(task_num), " in exam #", str(exam_num), " has a negativ of maximum points")

                if task.deduction_per_error < 0:
                    raise ValueError("In task ", str(task_num), " in exam #", str(exam_num), " deduction_per_error should be positiv (including zero)")

                if task.expected_answer.isspace() or len(task.expected_answer) <= 0:
                    raise ValueError("Task ", str(task_num), " in exam #", str(exam_num), " has no expected answer")
