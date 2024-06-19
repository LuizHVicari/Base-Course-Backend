from django.db import models

from .category_model import Category


class Course(models.Model):
  title = models.CharField(max_length=50)
  description = models.TextField(blank=True, null=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  cover = models.ImageField(upload_to='courses/', blank=True, null=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  
  def __str__(self) -> str:
      return self.title