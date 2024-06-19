from rest_framework import serializers

from course.models import Category


class CategorySerializerV1(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id', 'name', 'description', 'color', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']