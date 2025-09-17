import json
from datetime import timezone

from django.db.models import Expression
from django.http import JsonResponse
from ...domain.entities import LessonParams
from ...domain.services.services import ILessonsService
from ...interfaces.api.dto import CreateLessonsRequestDTO, CreateLessonResponseDTO
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def lessons_view(lessons_service: ILessonsService):
    @csrf_exempt
    @require_POST
    def create_lessons(request):
        try:
            json_body = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "invalid JSON"}, status=400)

        params: list[LessonParams] = []

        for c in json_body:
            serializer = CreateLessonsRequestDTO(data=c)
            if not serializer.is_valid():
                return JsonResponse({"error": "serialization failed"}, status=400)

            param = LessonParams(
                start_time=serializer.validated_data["start_time"].astimezone(timezone.utc),
                lesson_level=serializer.validated_data["lesson_level"],
                lesson_name=serializer.validated_data["lesson_name"],
                max_capacity=serializer.validated_data["max_capacity"],
                location=serializer.validated_data["location"],
            )

            params.append(param)

        #TODO: handle this error
        inserted_lessons = lessons_service.create_lessons(params)

        try:
            resp = [CreateLessonResponseDTO.from_domain(c).data for c in inserted_lessons]
        except Expression as e:
            raise f"error: {e}"

        return JsonResponse({"lessons": resp})

    return create_lessons
