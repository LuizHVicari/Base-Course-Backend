from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import BadRequest
from django.http import Http404

from api.serializers import CommentSerializerV1
from course.models import Comment
from api.utils.pagination.pagination_classes import StandardPagination


most_recent_serializer = CommentSerializerV1


class CommentListCreate(ListCreateAPIView):
  permission_classes = [IsAuthenticatedOrReadOnly, ]
  pagination_class = StandardPagination

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CommentSerializerV1

    return most_recent_serializer
  

  def get_queryset(self):
    queryset = Comment.objects.all()
    user : str | None = self.request.query_params.get('user')
    lesson : str | None = self.request.query_params.get('lesson')
    stars : str | None = self.request.query_params.get('stars')

    if lesson == None and stars != None:
      raise BadRequest('cannot filter stars without a lesson')
    
    if user != None:
      queryset = queryset.filter(user__username__icontains=user)
    if lesson != None:
      queryset = queryset.filter(lesson__title__icontains=lesson)
    if stars != None:
      queryset = queryset.filter(stars=int(stars))

    if not queryset: raise Http404
    return queryset
    

class CommentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  queryset = Comment.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CommentSerializerV1

    return most_recent_serializer
