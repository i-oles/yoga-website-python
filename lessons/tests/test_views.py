import datetime
import uuid
import pytest
import json
from datetime import timedelta
from unittest.mock import patch
from django.test import Client

from lessons.domain.entities import Lesson


test_lesson_id = uuid.uuid4()
test_future_date = datetime.datetime.now(datetime.timezone.utc) + timedelta(days=2)


@patch("lessons.interfaces.api.views.ILessonsService")
@pytest.mark.django_db
def test_create_lessons_success(mock_service):
    mock_service.return_value.create_lessons.return_value = [
        Lesson(
            id=test_lesson_id,
            start_time=test_future_date,
            lesson_name="vinyasa",
            lesson_level="intermediate",
            max_capacity=10,
            current_capacity=10,
            location="home",
        ),
    ]

    client = Client()
    body = [
        {
            "start_time": "2025-09-20T10:00:00Z",
            "lesson_level": "intermediate",
            "lesson_name": "vinyasa",
            "max_capacity": 10,
            "location": "home"
        }
    ]

    response = client.post(
        "/api/v1/lessons/",
        data=json.dumps(body),
        content_type="application/json"
    )

    # assert response.status_code == 200
    data = response.json()
    print(data)

    assert data["lessons"][0]["id"] == str(test_lesson_id)
    # assert data["lessons"][0]["start_time"] == test_future_date.isoformat()
    # assert data["lessons"][0]["lesson_name"] == "vinyasa"
    # assert data["lessons"][0]["lesson_level"] == "intermediate"
    # assert data["lessons"][0]["max_capacity"] == 10
    # assert data["lessons"][0]["current_capacity"] == 10
    # assert data["lessons"][0]["location"] == "home"