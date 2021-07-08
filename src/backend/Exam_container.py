from dataclasses import dataclass

from Exam import Exam

@dataclass
class Exam_container:
    correct_exam: Exam
    student_exams: list[Exam]
