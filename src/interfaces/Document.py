from dataclasses import dataclass, field
from typing import List

from PIL import Image

from .Task import Task
from .task_types import Task_type


@dataclass()
class Document:
    img: Image = field(compare=False)
    tasks: List[Task] = field(default_factory=list, compare=True)
    img_modified: Image = field(default=None, compare=False, init=False)
    documents_to_check : List[Image] = field(default=None, compare=False, init=False)

    def __post_init__(self):
        self.img_modified=self.img

