from django.urls import path
from .views import lessons_view
from ...application.service.lessons import LessonsService
from ...infrastructure.sqlite.lessons import LessonsRepo

urlpatterns = [
    path("", lessons_view(LessonsService(LessonsRepo())))
]
