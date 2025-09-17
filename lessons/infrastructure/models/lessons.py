from django.db import models


class LessonModel(models.Model):
    id = models.UUIDField(primary_key=True),
    start_time = models.DateTimeField()
    lesson_level = models.CharField(max_length=40)
    lesson_name = models.CharField(max_length=30)
    max_capacity = models.IntegerField()
    location = models.CharField(max_length=30)
