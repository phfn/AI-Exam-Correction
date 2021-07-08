from dataclasses import dataclass, field
from PIL import Image
from Task import Task

@dataclass
class Exam:

    image: Image = field(compare=False)
    tasks: list[Task] = field(compare=True, init=True)
    image_modified : Image = field(default=None, compare=False, init=False)

    def __post_init__(self):
        self.image_modified = self.image
