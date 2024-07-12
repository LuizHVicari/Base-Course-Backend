from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import SaveFactory, UserFactory
from course.models import Save
from api.serializers import SaveSerializerV1
from backend.faker_base import faker


class TestAuthUserComments(APITestCase):
  def setUp(self):
    faker.unique.clear()
    self.save_1 = SaveFactory()
    self.save_2 = SaveFactory()
    for _ in range(10):
      SaveFactory()

    self.user = UserFactory()
    self.save_3 = SaveFactory(user=self.user)

    self.client = APIClient()
    self.client.force_authenticate(user=self.user)
    self.client.credentials(HTTP_ACCEPT='application/json; version=v1')

  
  def test_auth_user_can_save_lessons(self):
    lesson = self.save_1.lesson
    response = self.client.post(
      path=reverse('saves'),
      data={
        'lesson': lesson.id
      })
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Save.objects.count(), 14)

  
  def test_auth_user_can_list_his_saves(self):
    response = self.client.get(path=reverse('saves'))
    saves = Save.objects.filter(user=self.user)
    serializer = SaveSerializerV1(saves, many=True)
    
    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_auth_user_can_retrieve_his_saves(self):
    response = self.client.get(path=reverse('save', args=[self.save_3.id]))
    save = Save.objects.get(pk=response.data.get('id'))
    serializer = SaveSerializerV1(save)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, serializer.data)

  
  def test_auth_user_cannot_retrieve_others_saves(self):
    response = self.client.get(path=reverse('save', args=[self.save_1.id]))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_auth_user_can_delete_his_saves(self):
    response = self.client.delete(path=reverse('save', args=[self.save_3.id]))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Save.objects.count(), 12)
    self.assertEqual(Save.objects.filter(user=self.user).count(), 0)

  
  def test_auth_user_can_not_delete_others_saves(self):
    response = self.client.delete(path=reverse('save', args=[self.save_1.id]))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(Save.objects.count(), 13)
    self.assertEqual(Save.objects.filter(user=self.user).count(), 1)

  
  def test_auth_user_cannot_save_same_lesson_twice(self):
    lesson = self.save_3.lesson
    response = self.client.post(
      path=reverse('saves'),
      data={
        'lesson': lesson.id
      })
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(Save.objects.count(), 13)
    self.assertEqual(Save.objects.filter(user=self.user).count(), 1)