from dataclasses import dataclass, field
from PIL import Image
from Task import Task

@dataclass()
class Exam:

    img : Image = field(compare=False)
    img_modified : Image = field(default=None, compare=False, init=False)
    tasks : list[Task] = field(default_factory=list, compare=True)

    def __post_init__(self, tasks : list[Task]):
        self.img_modified = self.img
        self.tasks = tasks
