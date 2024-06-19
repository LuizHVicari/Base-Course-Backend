from rest_framework import serializers

from course.models import Lesson


class LessonSerializerV1(serializers.ModelSerializer):
  class Meta:
    model = Lesson
    fields = ['id', 'title', 'description', 'course', 'cover', 'video', 'text', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']

  