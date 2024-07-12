from rest_framework import serializers
from django.core.exceptions import ValidationError

from course.models import Watched


class WatchedSerializerV1(serializers.ModelSerializer):
  class Meta:
    model = Watched
    fields = ['id', 'user', 'lesson', 'watched_time', 'created_at', 'updated_at']
    read_only_fields = ['id', 'user', 'created_at', 'updated_at']


  def create(self, validated_data):
    try:
      watched = Watched(
        user = self.context.get('request').user,
        lesson = validated_data.get('lesson'),
        watched_time = validated_data.get('watched_time')
      )
      watched.full_clean()
      watched.save()
    except ValidationError as e:
      raise serializers.ValidationError(e)
    return watched