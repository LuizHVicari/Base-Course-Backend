from django.contrib.auth.models import User
from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
  """
  Custom permission to only allow staff users to modify data.
  """
  message = 'only staff users can modify this data'
  def has_permission(self, request, view):
    if request.user.is_superuser or request.user.is_staff:
      return True
    if request.METHOD in permissions.SAFE_METHODS:
      return True
    return False