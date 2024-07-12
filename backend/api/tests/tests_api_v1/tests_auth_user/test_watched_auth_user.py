from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import WatchedFactory, UserFactory
from course.models import Watched
from api.serializers import WatchedSerializerV1
from backend.faker_base import faker


class TestAuthUserComments(APITestCase):
  def setUp(self):
    faker.unique.clear()
    self.watched_1 = WatchedFactory()
    self.watched_2 = WatchedFactory()
    for _ in range(10):
      WatchedFactory()

    self.user = UserFactory()
    self.watched_3 = WatchedFactory(user=self.user)

    self.client = APIClient()
    self.client.credentials(HTTP_ACCEPT='application/json; version=v1')

  
  def test_auth_user_can_list_his_watcheds(self):
    response = self.client.get(path=reverse('watcheds'))
    watcheds = Watched.objects.filter(user=self.user)
    serializer = WatchedSerializerV1(watcheds, many=True)
    
    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_auth_user_can_retrieve_his_watcheds(self):
    response = self.client.get(path=reverse('watched', args=[self.watched_3.id]))
    watched = Watched.objects.get(pk=response.data.get('id'))
    serializer = WatchedSerializerV1(watched)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, serializer.data)

  
  def test_auth_user_cannot_retrieve_others_watcheds(self):
    response = self.client.get(path=reverse('watched', args=[self.watched_1.id]))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_auth_user_can_update_his_watcheds(self):
    response = self.client.put(
      path=reverse('watched', args=[self.watched_3.id]),
      data={
        'user': self.watched_3.user.username,
        'lesson': self.watched_3.lesson.title
      })
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_auth_user_cannot_update_others_watcheds(self):
    response = self.client.put(
      path=reverse('watched', args=[self.watched_1.id]),
      data={
        'user': self.watched_1.user.username,
        'lesson': self.watched_1.lesson.title
      })
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


  def test_auth_user_can_patch_his_watcheds(self):
    response = self.client.patch(
      path=reverse('watched', args=[self.watched_3.id]),
      data={
        'user': self.watched_3.user.username,
        'lesson': self.watched_3.lesson.title
      })
    self.assertEqual(response.status_code, status.HTTP_200_OK)


  def test_auth_user_cannot_patch_others_watcheds(self):
    response = self.client.patch(
      path=reverse('watched', args=[self.watched_1.id]),
      data={
        'user': self.watched_1.user.username,
        'lesson': self.watched_1.lesson.title
      })
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_auth_user_can_delete_his_watcheds(self):
    response = self.client.delete(path=reverse('watched', args=[self.watched_3.id]))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Watched.objects.count(), 12)
    self.assertEqual(Watched.objects.filter(user=self.user).count(), 0)

  
  def test_auth_user_cannot_delete_others_watcheds(self):
    response = self.client.delete(path=reverse('watched', args=[self.watched_1.id]))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(Watched.objects.count(), 13)
    self.assertEqual(Watched.objects.filter(user=self.user).count(), 1)

  