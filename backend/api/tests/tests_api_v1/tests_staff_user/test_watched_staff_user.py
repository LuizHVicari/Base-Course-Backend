from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import WatchedFactory, UserFactory
from course.models import Watched
from api.serializers import WatchedSerializerV1
from backend.faker_base import faker


class TestStaffUserWatcheds(APITestCase):
  def setUp(self):
    faker.unique.clear()
    self.watched_1 = WatchedFactory()
    self.watched_2 = WatchedFactory()
    for _ in range(10):
      WatchedFactory()

    self.user = UserFactory()
    self.user.is_staff = True
    self.user.save()
    self.watched_3 = WatchedFactory(user=self.user)

    self.client = APIClient()
    self.client.force_authenticate(user=self.user)
    self.client.credentials(HTTP_ACCEPT='application/json; version=v1')

  
  def test_staff_user_can_list_all_watcheds(self):
    response = self.client.get(path=reverse('watcheds'))
    watcheds = Watched.objects.all()
    serializer = WatchedSerializerV1(watcheds, many=True)
    
    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_staff_user_can_post_watcheds(self):
    response = self.client.post(
      path=reverse('watcheds'),
      data={
        'lesson': self.watched_1.lesson.id,
        'watched_time': 100
      })
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Watched.objects.count(), 14)

  
  def test_staff_user_can_retrieve_watcheds(self):
    response = self.client.get(path=reverse('watched', args=[self.watched_1.id]))
    watched = Watched.objects.get(pk=self.watched_1.id)
    serializer = WatchedSerializerV1(watched)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, serializer.data)

  
  def test_staff_user_cannot_retrieve_watched_that_does_not_exist(self):
    response = self.client.get(path=reverse('watched', args=[999]))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_staff_user_can_delete_watcheds(self):
    response = self.client.delete(path=reverse('watched', args=[self.watched_1.id]))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Watched.objects.count(), 12)

  
  def test_staff_user_can_update_watcheds(self):
    response = self.client.put(
      path=reverse('watched', args=[self.watched_1.id]),
      data={
        'lesson': self.watched_1.lesson.id,
        'watched_time': 100
      })
    watched = Watched.objects.get(pk=self.watched_1.id)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(watched.watched_time, 100)

  
  def test_staff_user_can_patch_watcheds(self):
    response = self.client.patch(
      path=reverse('watched', args=[self.watched_1.id]),
      data={
        'lesson': self.watched_1.lesson.id
      })
    watched = Watched.objects.get(pk=self.watched_1.id)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(watched.lesson, self.watched_1.lesson)