from abc import abstractmethod, ABC

from lessons.domain.entities import Lesson


class ILessonsRepository(ABC):
    @abstractmethod
    def insert(self, lessons: list[Lesson]) -> list[Lesson]:
        return lessons

