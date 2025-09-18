import datetime
import uuid
import json
import pytest
from datetime import timedelta
from unittest.mock import MagicMock
from django.test import RequestFactory, Client
from django.http import JsonResponse

from lessons.domain.entities import Lesson
from lessons.interfaces.api.dto import translate_week_day_to_polish
from lessons.interfaces.api.views import lessons_view

test_lesson_id = uuid.uuid4()
now = datetime.datetime.now(datetime.timezone.utc)
future_date = now + timedelta(days=2)


def parse_json(response):
    if isinstance(response, JsonResponse):
        return json.loads(response.content)
    return response.json()


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def factory():
    return RequestFactory()


def test_create_lessons_success(mock_service, factory):
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
    data = parse_json(response)

    assert response.status_code == 200
    assert data["lessons"][0] == {
        "id": str(test_lesson_id),
        "week_day": translate_week_day_to_polish(future_date.weekday()),
        "start_date": future_date.strftime('%d-%m-%y'),
        "start_hour": future_date.strftime('%H:%M'),
        "lesson_name": "vinyasa",
        "lesson_level": "intermediate",
        "max_capacity": 10,
        "current_capacity": 10,
        "location": "home",
    }

@pytest.mark.django_db
def test_create_lessons_location_too_short(client: Client):
    body = [
        {
            "start_time": future_date.isoformat(),
            "lesson_level": "intermediate",
            "lesson_name": "vinyasa",
            "max_capacity": 10,
            "location": "h"
        }
    ]

    response = client.post(
        "/api/v1/lessons/",
        data=json.dumps(body),
        content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json()["message"] == "serialization failed"
