from django.db import models
from django.contrib.auth.models import User

from .class_model import Class


class Watched(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  class_field = models.ForeignKey(Class, on_delete=models.CASCADE)
  Watched_time = models.IntegerField(default=0)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def __str__(self) -> str:
    return f'{self.user.username} - {self.class_field.title}'
    