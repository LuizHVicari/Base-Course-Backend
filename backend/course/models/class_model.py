from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from .course_model import Course


class Class(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField(blank=True, null=True)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	cover = models.ImageField(upload_to='classes/', blank=True, null=True)
	video = models.FileField(upload_to='classes/', blank=True, null=True)
	text = CKEditor5Field(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self) -> str:
			return self.title