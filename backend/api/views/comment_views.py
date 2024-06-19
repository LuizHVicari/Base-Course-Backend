from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import CommentSerializerV1
from course.models import Comment
from api.utils.pagination.pagination_classes import StandardPagination


most_recent_serializer = CommentSerializerV1


class CommentListCreate(ListCreateAPIView):
  queryset = Comment.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]
  pagination_class = StandardPagination

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CommentSerializerV1

    return most_recent_serializer
  

class CommentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  queryset = Comment.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CommentSerializerV1

    return most_recent_serializer