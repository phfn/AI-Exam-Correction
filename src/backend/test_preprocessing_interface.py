import preprocessing_interface
from PIL import Image
from Exam_container import Exam_container
from Task import Task
from task_types import Task_type
from Exam import Exam

img = Image.open("./test_images/testbob.png")

tasks = [Task(1125, 965, 790, 225, Task_type.TEXT, "ANSWER", 100.0, 20.0, "", 0)]
# error_tasks = [Task(1125, 965, 790, -1, Task_type.TEXT, "", 1, 1, "", 0)]
# error_document = Exam_container(img, error_tasks, exams)

exams_students = [Exam(img, tasks)]

exam_container = Exam_container(
        Exam(img, tasks),
        exams_students
        )

def test_autocorrect_exams():
    assert preprocessing_interface.autocorrect_exams(exam_container)
    
def test_autodetect_expectet_answers():
    assert preprocessing_interface.autodetect_expected_answers(exam_container) 
