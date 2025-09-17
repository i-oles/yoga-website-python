from lessons.domain.repositories.repositories import ILessonsRepository
from lessons.domain.entities import Lesson


class LessonsRepo(ILessonsRepository):
    def __init__(self):
        pass

    def insert(self, lesson: list[Lesson]) -> list[Lesson]:
        # TODO: implement me
        return lesson
