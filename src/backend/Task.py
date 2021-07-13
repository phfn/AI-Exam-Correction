from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config, LetterCase

from task_types import Task_type, from_str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Task:
    """Object that describes tasks contained in a document"""
    x: int
    y: int
    width: int
    height: int
    type: Task_type = field(metadata=config(decoder=from_str, encoder=str))
    expected_answer: str
    max_points: float
    deduction_per_error: float = 0
    actual_answer: str = ""
    points: float = 0
