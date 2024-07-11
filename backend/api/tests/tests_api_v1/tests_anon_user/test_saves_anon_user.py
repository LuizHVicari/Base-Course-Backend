from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import SaveFactory
from course.models import Save
from api.serializers import SaveSerializerV1
from backend.faker_base import faker


class TestAnonUserComments(APITestCase):
  def setUp(self):
    self.save_1 = SaveFactory()
    self.save_2 = SaveFactory()
    for _ in range(10):
      SaveFactory()

    self.client = APIClient()

  def test_anon_user_cannot_list_saves(self):
    response = self.client.get(path=reverse('saves'))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_post_save(self):
    response = self.client.post(
      path=reverse('saves'), 
      data={
        'user': self.save_1.user.username,
        'lesson': self.save_1.lesson.title
      })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_retrieve_save(self):
    response = self.client.get(path=reverse('save', kwargs={'pk': self.save_1.pk}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_update_save(self):
    response = self.client.put(
      path=reverse('save', kwargs={'pk': self.save_1.pk}),
      data={
        'user': self.save_1.user.username,
        'lesson': self.save_1.lesson.title
      })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_delete_save(self):
    response = self.client.delete(path=reverse('save', kwargs={'pk': self.save_1.pk}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_update_partially_save(self):
    response = self.client.patch(
      path=reverse('save', kwargs={'pk': self.save_1.pk}),
      data={
        'user': self.save_1.user.username,
        'lesson': self.save_1.lesson.title
      })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)