import uuid
from datetime import timezone

from django.utils import timezone

from lessons.domain.entities import LessonParams, Lesson
from lessons.domain.exceptions import BusinessError
from lessons.domain.repositories.repositories import ILessonsRepository
from lessons.domain.services.services import ILessonsService


class LessonsService(ILessonsService):
    def __init__(self, lessons_repo: ILessonsRepository):
        self.lessons_repo = lessons_repo
        pass

    def create_lessons(self, lesson_params: list[LessonParams]) -> list[Lesson]:
        validate_params(lesson_params)

        lessons = [
            Lesson(
                id=uuid.uuid4(),
                start_time=p.start_time,
                lesson_level=p.lesson_level,
                lesson_name=p.lesson_name,
                max_capacity=p.max_capacity,
                current_capacity=p.max_capacity,
                location=p.location,
            ) for p in lesson_params]

        inserted_lessons = self.lessons_repo.insert(lessons)

        return inserted_lessons


def validate_params(params: list[LessonParams]):
    for param in params:
        if param.start_time < timezone.now():
            raise BusinessError(
                message=f"Cannot create lesson in the past (start_time={param.start_time})",
            )

    return
