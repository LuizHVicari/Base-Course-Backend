from django.urls import path, include

from .views import (
  CategoryListCreate, CategoryRetrieveUpdateDestroy, 
  CourseListCreate, CourseRetrieveUpdateDestroy
  )


category_paths = [
  path('', CategoryListCreate.as_view(), name='categories'),
  path('<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category')
]

course_paths = [
  path('', CourseListCreate.as_view(), name='courses'),
  path('<int:pk>/', CourseRetrieveUpdateDestroy.as_view(), name='course')
]

urlpatterns = [
  path('category/', include(category_paths)),
  path('courses/', include(course_paths)),
]
