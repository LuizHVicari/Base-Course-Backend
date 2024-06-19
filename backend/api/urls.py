from django.urls import path, include

from .views import (
  CategoryListCreate, CategoryRetrieveUpdateDestroy, 
  CourseListCreate, CourseRetrieveUpdateDestroy,
  LessonListCreate, LessonRetrieveUpdateDestroy,
  CommentListCreate, CommentRetrieveUpdateDestroy,
  SaveListCreate, SaveRetrieveUpdateDestroy
  )


category_paths = [
  path('', CategoryListCreate.as_view(), name='categories'),
  path('<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category')
]

course_paths = [
  path('', CourseListCreate.as_view(), name='courses'),
  path('<int:pk>/', CourseRetrieveUpdateDestroy.as_view(), name='course')
]

lesson_paths = [
  path('', LessonListCreate.as_view(), name='lessons'),
  path('<int:pk>', LessonRetrieveUpdateDestroy.as_view(), name='lesson')
]

comment_paths = [
  path('', CommentListCreate.as_view(), name='comments'),
  path('<int:pk>', CommentRetrieveUpdateDestroy.as_view(), name='comment')
]

save_paths = [
  path('', SaveListCreate.as_view(), name='saves'),
  path('<int:pk>', SaveRetrieveUpdateDestroy.as_view(), name='save')
]

urlpatterns = [
  path('categories/', include(category_paths)),
  path('courses/', include(course_paths)),
  path('lessons/', include(lesson_paths)),
  path('comments/', include(comment_paths)),
  path('saves/', include(save_paths)),
]
