from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from .lesson_model import Lesson


class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
  text = models.TextField(blank=True, null=True)
  stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True, null=True)
  comment_fk = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def __str__(self) -> str:
    return self.user.username + self.text
  

  def clean(self):
    if self.comment_fk == self:
        raise ValidationError('Comment cannot be a parent of itself')
    if self.comment_fk == None and self.lesson == None:
        raise ValidationError('Comment must have a parent or a lesson')
    if self.comment_fk != None and self.lesson != None:
        raise ValidationError('Comment cannot have a parent and a lesson')