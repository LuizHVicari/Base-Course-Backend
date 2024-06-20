from rest_framework import serializers

from course.models import Watched


class WatchedSerializerV1(serializers.ModelSerializer):
  class Meta:
    model = Watched
    fields = ['id', 'user', 'lesson', 'watched_time', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']