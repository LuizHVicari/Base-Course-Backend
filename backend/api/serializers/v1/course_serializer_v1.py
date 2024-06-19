from rest_framework import serializers

from course.models import Course


class CourseSerializerV1(serializers.ModelSerializer):
  class Meta:
    model = Course
    fields = ['id', 'title', 'description', 'category', 'cover', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']