from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config, LetterCase
from PIL.Image import Image
from Task import Task
from base64converter import base_64_to_PIL_Image, PIL_Image_to_base_64


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Exam:
    '''
    Class for storing an exam.

    The attributes of an exam are:
        - Image of the exam.
        - Filename 
        - List of tasks (see task.py)
        - Modified image for user feedback
    '''

    image: Image = field(
            compare=False,
            # required for json converting
            metadata=config(
                encoder=PIL_Image_to_base_64,
                decoder=base_64_to_PIL_Image
            )
        )
    filename: str
    tasks: list[Task] = field(compare=True, init=True)
    image_modified: Image = field(
            default=None,
            compare=False,
            init=False,
            # required for json converting
            metadata=config(
                encoder=PIL_Image_to_base_64,
                decoder=base_64_to_PIL_Image
            )
        )

    def __post_init__(self):
        self.image_modified = self.image
