from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from Exam import Exam


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Exam_container:
    '''
    Main class for communication.

    This class contains a correct exam that should contain the model solution and a list of 
    exams that need correction.
    '''
    correct_exam: Exam
    student_exams: list[Exam]
