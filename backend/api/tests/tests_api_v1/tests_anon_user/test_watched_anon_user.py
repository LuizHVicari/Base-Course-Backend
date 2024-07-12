from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import WatchedFactory
from course.models import Watched
from api.serializers import WatchedSerializerV1
from backend.faker_base import faker


class TestAnonUserComments(APITestCase):
  def setUp(self):
    self.watched_1 = WatchedFactory()
    self.watched_2 = WatchedFactory()
    for _ in range(10):
      WatchedFactory()

    self.client = APIClient()
    self.client.credentials(HTTP_ACCEPT='application/json; version=v1')


  def test_anon_user_cannot_list_watched(self):
    response = self.client.get(path=reverse('watcheds'))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_filter_watched_by_lesson(self):
    response = self.client.get(
      path=reverse('watcheds'), 
      QUERY_STRING=f'lesson={self.watched_1.lesson.title}')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_post_watched(self):
    response = self.client.post(
      path=reverse('watcheds'), 
      data={
        'user': self.watched_1.user.username,
        'lesson': self.watched_1.lesson.title
      })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_retrieve_watched(self):
    response = self.client.get(path=reverse('watched', kwargs={'pk': self.watched_1.pk}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_update_watched(self):
    response = self.client.put(
      path=reverse('watched', kwargs={'pk': self.watched_1.pk}),
      data={
        'user': self.watched_1.user.username,
        'lesson': self.watched_1.lesson.title
      })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_delete_watched(self):
    response = self.client.delete(path=reverse('watched', kwargs={'pk': self.watched_1.pk}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_update_partially_watched(self):
    response = self.client.patch(
      path=reverse('watched', kwargs={'pk': self.watched_1.pk}),
      data={
        'user': self.watched_1.user.username,
        'lesson': self.watched_1.lesson.title
      })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)