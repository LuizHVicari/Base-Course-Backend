from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from .class_model import Class


class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.TextField(blank=True, null=True)
  stars = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
  class_fk = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
  comment_fk = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def __str__(self) -> str:
      return self.user.username + self.text