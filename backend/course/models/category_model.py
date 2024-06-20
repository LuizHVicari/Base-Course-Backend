from django.db import models

from .utils.validators import validate_not_numeric


class Category(models.Model):
  name = models.CharField(max_length=50, unique=True, validators=[validate_not_numeric, ])
  description = models.TextField(blank=True, null=True)
  color = models.CharField(max_length=7, default="#000000")

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def __str__(self) -> str:
    return self.name
  