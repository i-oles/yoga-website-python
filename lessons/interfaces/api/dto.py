from rest_framework import serializers

from lessons.domain.entities import Lesson


class CreateLessonResponseDTO(serializers.Serializer):
    id = serializers.UUIDField()
    week_day = serializers.CharField(allow_null=False)
    start_date = serializers.DateField(format="%d-%m-%y", allow_null=False)
    start_hour = serializers.TimeField(format="%H:%M", allow_null=False)
    lesson_level = serializers.CharField(min_length=3, max_length=40, allow_blank=False)
    lesson_name = serializers.CharField(min_length=3, max_length=40, allow_blank=False)
    current_capacity = serializers.IntegerField()
    max_capacity = serializers.IntegerField()
    location = serializers.CharField(min_length=5, allow_blank=False)

    @classmethod
    def from_domain(cls, lesson: Lesson) -> "CreateLessonResponseDTO":
        return cls({
            "id": lesson.id,
            "week_day": translate_week_day_to_polish(lesson.start_time.weekday()),
            "start_date": lesson.start_time.date(),
            "start_hour": lesson.start_time.time(),
            "lesson_level": lesson.lesson_level,
            "lesson_name": lesson.lesson_name,
            "current_capacity": lesson.current_capacity,
            "max_capacity": lesson.max_capacity,
            "location": lesson.location,
        })

class CreateLessonsRequestDTO(serializers.Serializer):
    start_time = serializers.DateTimeField(format="iso-8601", required=True)
    lesson_level = serializers.CharField(min_length=3, max_length=40, allow_blank=False)
    lesson_name = serializers.CharField(min_length=3, max_length=40, allow_blank=False)
    max_capacity = serializers.IntegerField(min_value=1, allow_null=False)
    location = serializers.CharField(min_length=5, allow_blank=False)


def translate_week_day_to_polish(week_day: int) -> str:
    days = [
        "poniedziałek",
        "wtorek",
        "środa",
        "czwartek",
        "piątek",
        "sobota",
        "niedziela",
    ]

    try:
        return days[week_day]
    except IndexError:
        raise ValueError("unknown week day")
