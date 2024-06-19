from django.db import models
from django.contrib.auth.models import User

from .class_model import Class


class Save(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  class_fk = models.ForeignKey(Class, on_delete=models.CASCADE)