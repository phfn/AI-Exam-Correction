from dataclasses import dataclass, field
from PIL import Image
from Task import Task

@dataclass()
class Exam:

    img : Image = field(compare=False)
    img_modified : Image = field(default=None, compare=False, init=False)
    tasks : list[Task] = field(default_factory=list, compare=True)

    def __init__(self, img : Image, tasks : list[Task]):
        self.img = img
        self.img_modified = img
        self.tasks = tasks
