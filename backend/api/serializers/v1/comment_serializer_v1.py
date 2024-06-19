from rest_framework import serializers

from course.models import Comment


class CommentSerializerV1(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['id', 'user', 'lesson', 'text', 'stars', 'comment_fk', 'created_at', 'updated_at']
    read_only_feilds = ['id', 'created_at', 'updated_at']