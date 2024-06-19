from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from .lesson_model import Lesson


class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
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
    try: 
      if self.comment_fk != None and self.comment_fk.lesson != self.lesson:
        raise ValidationError('Comment must be from the same lesson as its parent')
    except (Comment.DoesNotExist, Lesson.DoesNotExist):
      raise ValidationError('Comment must have a valid parent')