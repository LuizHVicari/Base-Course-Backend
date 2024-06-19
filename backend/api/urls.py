from django.urls import path, include

from .views import CategoryListCreate, CategoryRetrieveUpdateDestroy

category_paths = [
  path('', CategoryListCreate.as_view(), name='categories'),
  path('<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category')
]

urlpatterns = [
  path('category/', include(category_paths)),
]
