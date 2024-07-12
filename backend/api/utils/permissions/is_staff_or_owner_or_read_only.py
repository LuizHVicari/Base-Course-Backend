from django.contrib.auth.models import User
from rest_framework import permissions


class IsStaffOrOwnerOrReadOnly(permissions.BasePermission):
  """
  Custom permission to only allow staff users or the user that data is related to modify it.
  Assumes that the model instance has a `user` attribute.
  Only implements object permission check, not view permission check.
  """
  message = 'only staff users or the user that data is related to can modify this data'

  def has_object_permission(self, request, view, obj):
    if request.user.is_superuser or request.user.is_staff:
      return True
    if obj.user == request.user:
      return True
    if request.method in permissions.SAFE_METHODS:
      return True
    return False