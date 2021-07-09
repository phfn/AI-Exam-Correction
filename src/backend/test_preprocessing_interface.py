import preprocessing_interface
from PIL import Image
from Exam_container import Exam_container
from Task import Task
from task_types import Task_type
from Exam import Exam

img = Image.open("./test_files/testbob.png")

tasks = [Task(1125, 965, 790, 225, Task_type.TEXT, "ANSWER", 100.0, 20.0, "", 0)]
# error_tasks = [Task(1125, 965, 790, -1, Task_type.TEXT, "", 1, 1, "", 0)]
# error_document = Exam_container(img, error_tasks, exams)

exams_students = [Exam(img, tasks)]

exam_container = Exam_container(
        Exam(img, tasks),
        exams_students
        )

def test_autocorrect_exams():
    text_task_types = [Task_type.NUMBER, Task_type.TEXT, Task_type.TEXT_NO_NUMBERS]

    for tasktype in text_task_types:
        for task_index, task in enumerate(exam_container.correct_exam.tasks):
            exam_container.correct_exam.tasks[task_index].type = tasktype
            
            for exam_index, exam in enumerate(exam_container.student_exams):
                for student_task_index, student_tasks in enumerate(exam.tasks):
                    exam_container.student_exams[exam_index].tasks[student_task_index].type = tasktype
                    preprocessing_interface.autocorrect_exams(exam_container)

def test_autodetect_expectet_answers():
    text_task_types = [Task_type.NUMBER, Task_type.TEXT, Task_type.TEXT_NO_NUMBERS]

    for tasktype in text_task_types:
        for task_index, task in enumerate(exam_container.correct_exam.tasks):
            exam_container.correct_exam.tasks[task_index].type = tasktype

            preprocessing_interface.autodetect_expected_answers(exam_container) 
