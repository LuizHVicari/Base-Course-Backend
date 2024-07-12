from rest_framework import serializers
from django.core.exceptions import ValidationError

from course.models import Save


class SaveSerializerV1(serializers.ModelSerializer):
  class Meta:
    model = Save
    fields = ['id', 'user', 'lesson', 'created_at', 'updated_at']
    read_only_fields = ['id', 'user' 'created_at', 'updated_at']

  
  def create(self, validated_data):
    try:
      save = Save(
        user = self.context.get('request').user,
        lesson = validated_data.get('lesson')
      )
      save.full_clean()
      save.save()
    except ValidationError as e:
      raise serializers.ValidationError(e)
    
    return save
