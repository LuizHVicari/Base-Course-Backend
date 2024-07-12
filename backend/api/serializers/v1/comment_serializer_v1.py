from rest_framework import serializers
from django.core.exceptions import ValidationError

from course.models import Comment


class CommentSerializerV1(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['id', 'user', 'lesson', 'text', 'stars', 'comment_fk', 'created_at', 'updated_at']
    read_only_feilds = ['id', 'user', 'created_at', 'updated_at']

  
  def create(self, validated_data):
    try:
      comment =  Comment(
        user = self.context.get('context').user,
        lesson = validated_data.get('lesson'),
        text = validated_data.get('text'),
        stars = validated_data.get('stars'),
        comment_fk = validated_data.get('comment_fk')
      )
      comment.full_clean()
      comment.save()
    
    except ValidationError as e:
      raise serializers.ValidationError(e)

    return comment