from abc import abstractmethod, ABC

from lessons.domain.entities import LessonParams, Lesson


class ILessonsService(ABC):
    @abstractmethod
    def create_lessons(self, lesson_params: list[LessonParams]) -> list[Lesson]:
        pass
