from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

from .course_model import Course
from .utils.validators.field_not_numeric_validator import validate_not_numeric


class Lesson(models.Model):
	title = models.CharField(max_length=50, unique=True, validators=[validate_not_numeric, ])
	description = models.TextField(blank=True, null=True)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	cover = models.ImageField(upload_to='classes/', blank=True, null=True)
	video = models.FileField(upload_to='classes/', blank=True, null=True)
	text = CKEditor5Field(blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self) -> str:
			return self.title
	

	def clean(self):
		if self.video == None and self.text == None:
			raise ValidationError('Lesson must have a video or text')