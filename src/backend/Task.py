from dataclasses import dataclass

from task_types import Task_type

@dataclass
class Task:
    """Object that describes tasks contained in a document"""
    x: int
    y: int
    width: int
    height: int
    type: Task_type
    expected_answer: str
    max_points: float
    deduction_per_error: float = 0
    actual_answer: str = ""
    points: float = 0
