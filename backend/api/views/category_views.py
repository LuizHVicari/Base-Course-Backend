from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.http import Http404

from api.serializers import CategorySerializerV1
from course.models import Category
from api.utils.pagination.pagination_classes import StandardPagination
from api.utils.permissions import IsStaffOrReadOnly


most_recent_serializer = CategorySerializerV1


class CategoryListCreate(ListCreateAPIView):
  permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrReadOnly, ]
  pagination_class = StandardPagination

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CategorySerializerV1
    
    return most_recent_serializer
  
  
  def get_queryset(self):
    queryset = Category.objects.all()
    name = self.kwargs.get('name')
    if name != None:
      queryset = queryset.filter(name__icontains=name)

    if not queryset: raise Http404
    return queryset.order_by('-updated_at')
  

class CategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrReadOnly, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CategorySerializerV1
    return most_recent_serializer
  

  def get_object(self):
    name = self.kwargs.get('name')
    if name != None:
      return get_object_or_404(Category, name=name)
    return get_object_or_404(Category, pk=self.kwargs.get('pk'))
    

  