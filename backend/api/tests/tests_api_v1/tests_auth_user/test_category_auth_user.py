from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import CategoryFactory, UserFactory
from course.models import Category
from api.serializers import CategorySerializerV1


class TestAuthUserCategory(APITestCase):
  def setUp(self):
    self.category_1 = CategoryFactory()
    self.category_2 = CategoryFactory()

    for _ in range(10):
      CategoryFactory()

    self.user = UserFactory()
    
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)
    self.client.credentials(HTTP_ACCEPT='application/json; version=v1')

  
  def test_auth_user_can_list_all_cateogries(self):
    response = self.client.get(path=reverse('categories'))
    categories = Category.objects.all()
    serializer = CategorySerializerV1(categories, many=True)
    
    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
