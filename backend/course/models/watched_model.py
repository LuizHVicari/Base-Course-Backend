from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from .lesson_model import Lesson


class Watched(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
  watched_time = models.IntegerField(default=0, validators=[MinValueValidator(0)])

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ('user', 'lesson')


  def __str__(self) -> str:
    return f'{self.user.username} - {self.lesson.title}'
    