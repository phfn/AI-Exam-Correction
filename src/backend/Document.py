from dataclasses import dataclass, field
from typing import List

from PIL import Image

from Task import Task
from task_types import Task_type
from Exam import Exam


@dataclass()
class Document:
    img: Image = field(compare=False)
    tasks: List[Task] = field(default_factory=list, compare=True)
    img_modified: Image = field(default=None, compare=False, init=False)
    exams : list = field(default_factory=list, compare=False, init=True)


    def add_exam(self, img : Image):
        exam = Exam(img, self.tasks) 
        self.exams.append(exam)

    def __post_init__(self):
        self.img_modified=self.img

