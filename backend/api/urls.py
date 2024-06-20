from django.urls import path, include, re_path

from .views import (
  CategoryListCreate, CategoryRetrieveUpdateDestroy, 
  CourseListCreate, CourseRetrieveUpdateDestroy,
  LessonListCreate, LessonRetrieveUpdateDestroy,
  CommentListCreate, CommentRetrieveUpdateDestroy,
  SaveListCreate, SaveRetrieveUpdateDestroy,
  WatchedListCreate, WatchedRetrieveUpdateDestroy
  )


category_paths = [
  path('', CategoryListCreate.as_view(), name='categories'),
  path('<str:name>/', CategoryListCreate.as_view(), name='categories'),
  path('only/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category'),
  path('only/<str:name>/', CategoryRetrieveUpdateDestroy.as_view(), name='category'),
]

course_paths = [
  path('', CourseListCreate.as_view(), name='courses'),
  re_path(
    '^(?P<title>.+)/^(?P<category>.+)/^(?P<max_lessons>[0-9]+)/^(?P<min_lessons>[0-9]+)/$',
    CourseListCreate.as_view(),
    name='courses'),
  path('only/<int:pk>/', CourseRetrieveUpdateDestroy.as_view(), name='course'),
  path('only/<str:title>/', CourseRetrieveUpdateDestroy.as_view(), name='course'),
]

lesson_paths = [
  path('', LessonListCreate.as_view(), name='lessons'),
  path('only/<int:pk>', LessonRetrieveUpdateDestroy.as_view(), name='lesson'),
]

comment_paths = [
  path('', CommentListCreate.as_view(), name='comments'),
  path('only/<int:pk>', CommentRetrieveUpdateDestroy.as_view(), name='comment'),
]

save_paths = [
  path('', SaveListCreate.as_view(), name='saves'),
  path('only/<int:pk>', SaveRetrieveUpdateDestroy.as_view(), name='save'),
]

watched_paths = [
  path('', WatchedListCreate.as_view(), name='watcheds'),
  path('only/<int:pk>', WatchedRetrieveUpdateDestroy.as_view(), name='watched'),
]

urlpatterns = [
  path('categories/', include(category_paths)),
  path('courses/', include(course_paths)),
  path('lessons/', include(lesson_paths)),
  path('comments/', include(comment_paths)),
  path('saves/', include(save_paths)),
  path('watcheds/', include(watched_paths)),
]
