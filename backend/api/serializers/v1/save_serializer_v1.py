from rest_framework import serializers

from course.models import Save


class SaveSerializerV1(serializers.ModelSerializer):
  class Meta:
    model = Save
    fields = ['id', 'user', 'lesson', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']