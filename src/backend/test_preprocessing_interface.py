import preprocessing_interface
from PIL import Image
from Exam_container import Exam_container
from Task import Task
from task_types import Task_type
from Exam import Exam
from pytest import raises
from copy import deepcopy


def test_autocorrect_exams():
    filename = "./test_files/testbob.png"
    img = Image.open(filename)

    text_task = Task(1125, 965, 790, 225, Task_type.TEXT, "ANSWER", 100.0, 20.0, "", 0)
    checkbox_task = Task(1125, 965, 790, 225, Task_type.SINGLE_CHOICE, "1", 100.0, 20.0, "1", 0)

    exams_students = [Exam(img, filename, [text_task])]

    exam_container = Exam_container(
            Exam(img, filename, [text_task]),
            exams_students
            )

    for tasktype in Task_type:
        for task_index, task in enumerate(exam_container.correct_exam.tasks):
            exam_container.correct_exam.tasks[task_index].type = tasktype

            if tasktype == Task_type.SINGLE_CHOICE or tasktype == Task_type.MULTIPLE_CHOICE:
                exam_container.correct_exam.tasks[task_index] = checkbox_task
            else: exam_container.correct_exam.tasks[task_index] = text_task
            
            for exam_index, exam in enumerate(exam_container.student_exams):
                for student_task_index, student_tasks in enumerate(exam.tasks):

                    if tasktype == Task_type.SINGLE_CHOICE or tasktype == Task_type.MULTIPLE_CHOICE:
                        exam_container.student_exams[exam_index].tasks[student_task_index]= checkbox_task
                    else: 
                        exam_container.student_exams[exam_index].tasks[student_task_index] = text_task

                    exam_container.student_exams[exam_index].tasks[student_task_index].type = tasktype

                    preprocessing_interface.autocorrect_exams(exam_container)

def test_autodetect_expectet_answers():
    filename = "./test_files/testbob.png"
    img = Image.open(filename)

    text_task = Task(1125, 965, 790, 225, Task_type.TEXT, "ANSWER", 100.0, 20.0, "", 0)
    checkbox_task = Task(1125, 965, 790, 225, Task_type.SINGLE_CHOICE, "1", 100.0, 20.0, "1", 0)


    exams_students = [Exam(img, filename, [text_task])]

    exam_container = Exam_container(
            Exam(img, filename, [text_task]),
            exams_students
            )

    for tasktype in Task_type:

        for task_index, task in enumerate(exam_container.correct_exam.tasks):
            if tasktype == Task_type.SINGLE_CHOICE or tasktype == Task_type.MULTIPLE_CHOICE:
                exam_container.correct_exam.tasks[task_index] = checkbox_task
            else: exam_container.correct_exam.tasks[task_index] = text_task

            exam_container.correct_exam.tasks[task_index].type = tasktype
            
            preprocessing_interface.autodetect_expected_answers(exam_container) 


def test_autodetect_expected_answers_error():
    filename = "./test_files/testbob.png"
    img = Image.open(filename)

    tasks = [Task(1125, 965, 790, 225, Task_type.TEXT, "ANSWER", 100.0, 20.0, "", 0)]

    exams_students = [Exam(img, filename, tasks)]

    exam_container = Exam_container(
            Exam(img, filename, tasks),
            exams_students
            )

    # Too slim image test
    with raises(FileNotFoundError): 
        error_exam_container = deepcopy(exam_container)
        error_exam_container.correct_exam.image = Image.open("test_files/too_slim_image.png")
        preprocessing_interface.autocorrect_exams(error_exam_container)

    # Too flat image
    with raises(FileNotFoundError):
        error_exam_container = deepcopy(exam_container)
        error_exam_container.correct_exam.image = Image.open("test_files/too_flat_image.png")
        preprocessing_interface.autodetect_expected_answers(error_exam_container)
    
    # Invalid task placement
    with raises(ValueError):
        error_exam_container = deepcopy(exam_container)
        error_exam_container.correct_exam.tasks[0].x = -1
        preprocessing_interface.autodetect_expected_answers(error_exam_container)

    # Invalid task placement
    with raises(ValueError):
        error_exam_container = deepcopy(exam_container)
        error_exam_container.correct_exam.tasks[0].y = -1
        preprocessing_interface.autodetect_expected_answers(error_exam_container)

    # Invalid size
    with raises(ValueError):
        error_exam_container = deepcopy(exam_container)
        error_exam_container.correct_exam.tasks[0].width = 0
        preprocessing_interface.autodetect_expected_answers(error_exam_container)

    # Invalid size
    with raises(ValueError):
        error_exam_container = deepcopy(exam_container)
        error_exam_container.correct_exam.tasks[0].height = 0
        preprocessing_interface.autodetect_expected_answers(error_exam_container)

    # Invalid points
    with raises(ValueError):
        error_exam_container = deepcopy(exam_container)
        error_exam_container.correct_exam.tasks[0].max_points = -1
        preprocessing_interface.autodetect_expected_answers(error_exam_container)
    
    # Invalid points
    with raises(ValueError):
        error_exam_container = deepcopy(exam_container)
        error_exam_container.correct_exam.tasks[0].deduction_per_error = -1
        preprocessing_interface.autodetect_expected_answers(error_exam_container)
    
