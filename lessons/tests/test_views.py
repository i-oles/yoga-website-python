import datetime
import uuid
import pytest
import json
from datetime import timedelta
from unittest.mock import MagicMock
from django.test import RequestFactory
from django.http import JsonResponse

from lessons.domain.entities import Lesson
from lessons.interfaces.api.dto import translate_week_day_to_polish
from lessons.interfaces.api.views import lessons_view

test_lesson_id = uuid.uuid4()
now = datetime.datetime.now(datetime.timezone.utc)
future_date = now + timedelta(days=2)

@pytest.mark.django_db
def test_create_lessons_success():
    mock_service = MagicMock()
    mock_service.create_lessons.return_value = [
        Lesson(
            id=test_lesson_id,
            start_time=future_date,
            lesson_name="vinyasa",
            lesson_level="intermediate",
            max_capacity=10,
            current_capacity=10,
            location="home",
        ),
    ]

    view_function = lessons_view(mock_service)

    factory = RequestFactory()
    body = [
        {
            "start_time": future_date.isoformat(),
            "lesson_level": "intermediate",
            "lesson_name": "vinyasa",
            "max_capacity": 10,
            "location": "home"
        }
    ]

    request = factory.post(
        "/api/v1/lessons/",
        data=json.dumps(body),
        content_type="application/json"
    )

    response = view_function(request)

    if isinstance(response, JsonResponse):
        data = json.loads(response.content)
    else:
        data = response.json()

    assert response.status_code == 200

    assert data["lessons"][0]["id"] == str(test_lesson_id)
    assert data["lessons"][0]["week_day"] == translate_week_day_to_polish(future_date.weekday())
    assert data["lessons"][0]["start_date"] == future_date.strftime('%d-%m-%y')
    assert data["lessons"][0]["start_hour"] == future_date.strftime('%H:%M')
    assert data["lessons"][0]["lesson_name"] == "vinyasa"
    assert data["lessons"][0]["lesson_level"] == "intermediate"
    assert data["lessons"][0]["max_capacity"] == 10
    assert data["lessons"][0]["current_capacity"] == 10
    assert data["lessons"][0]["location"] == "home"
