import preprocessing_interface as ppi
from PIL import Image
from Document import Document
from Task import Task
from task_types import Task_type
from pytest import raises
from Exam import Exam

img = Image.open("./test_images/testbob.png")

tasks = [Task(1125, 965, 790, 225, Task_type.TEXT, "ANSWER", 100.0, 20.0, "", 0)]
error_tasks = [Task(1125, 965, 790, -1, Task_type.TEXT, "", 1, 1, "", 0)]

exams = [Exam(img, tasks)]

document : Document = Document(img, tasks, exams)
error_document : Document = Document(img, error_tasks, exams)

def test_autocorrect_exams():
    assert ppi.autocorrect_exams(document)
    
def test_autodetect_expectet_answers() :
    assert ppi.autodetect_expected_answers(document) 

