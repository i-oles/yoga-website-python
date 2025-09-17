import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LessonParams:
    start_time: datetime
    lesson_level: str
    lesson_name: str
    max_capacity: int
    location: str


@dataclass
class Lesson:
    id: uuid.UUID
    start_time: datetime
    lesson_level: str
    lesson_name: str
    max_capacity: int
    current_capacity: int
    location: str
