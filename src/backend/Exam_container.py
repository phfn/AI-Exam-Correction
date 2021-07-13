from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from Exam import Exam


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Exam_container:
    correct_exam: Exam
    student_exams: list[Exam]
