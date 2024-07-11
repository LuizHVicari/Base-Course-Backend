from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import CategoryFactory
from course.models import Category
from api.serializers import CategorySerializerV1
from backend.faker_base import faker


class TestAnonUserCategories(APITestCase):
  def setUp(self):
    self.category_1 = CategoryFactory()
    self.category_2 = CategoryFactory()
    for _ in range(10):
      CategoryFactory()

    self.client = APIClient()

  
  def test_anon_user_can_list_all_categories(self):
    response = self.client.get(path=reverse('categories'))
    categories = Category.objects.all()
    serializer = CategorySerializerV1(categories, many=True)
    
    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_can_list_all_categories_by_name(self):
    response = self.client.get(path=reverse('categories', kwargs={'name': self.category_1.name}))
    categories = Category.objects.filter(name=self.category_1.name)
    serializer = CategorySerializerV1(categories, many=True)

    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)


  def test_anon_user_can_list_all_categories_by_partial_name(self):
    response = self.client.get(path=reverse('categories', kwargs={'name': self.category_1.name[:3]}))
    categories = Category.objects.filter(name__icontains=self.category_1.name[:3])
    serializer = CategorySerializerV1(categories, many=True)

    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)


  def test_anon_user_can_retrieve_any_cateogry(self):
    response = self.client.get(path=reverse('category', kwargs={'pk': self.category_1.pk}))
    category = Category.objects.get(pk=self.category_1.pk)
    serializer = CategorySerializerV1(category)

    self.assertEqual(response.data, serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_can_retrieve_any_category_by_name(self):
    response = self.client.get(path=reverse('category', kwargs={'name': self.category_1.name}))
    category = Category.objects.get(name=self.category_1.name)
    serializer = CategorySerializerV1(category)

    self.assertEqual(response.data, serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    

  def test_anon_user_cannot_retrieve_non_existent_category(self):
    response = self.client.get(path=reverse('category', kwargs={'pk': 999}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


  def test_anon_user_cannot_retrieve_non_existent_category_by_name(self):
    response = self.client.get(path=reverse('category', kwargs={'name': faker.unique.word()}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


  def test_anon_user_cannot_post_to_category(self):
    self.assertEqual(Category.objects.count(), 12)
    response = self.client.post(path=reverse('categories'), data={'name': faker.unique.word()})
    self.assertEqual(Category.objects.count(), 12)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_put_to_category(self):
    response = self.client.put(path=reverse('category', kwargs={'pk': self.category_1.pk}), data={'name': faker.unique.word(), 'description': faker.sentence(), 'color': faker.color()})
    not_updated_category = Category.objects.get(pk=self.category_1.pk)
    self.assertEqual(not_updated_category, self.category_1)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_put_to_category_by_name(self):
    response = self.client.put(path=reverse('category', kwargs={'name': self.category_1.name}), data={'name': faker.unique.word(), 'description': faker.sentence(), 'color': faker.color()})
    not_updated_category = Category.objects.get(pk=self.category_1.pk)
    self.assertEqual(not_updated_category, self.category_1)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_patch_to_category(self):
    response = self.client.patch(path=reverse('category', kwargs={'pk': self.category_1.pk}), data={'name': faker.unique.word()})
    not_updated_category = Category.objects.get(pk=self.category_1.pk)
    self.assertEqual(not_updated_category, self.category_1)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_patch_to_category_by_name(self): 
    response = self.client.patch(path=reverse('category', kwargs={'name': self.category_1.name}), data={'name': faker.unique.word()})
    not_updated_category = Category.objects.get(pk=self.category_1.pk)
    self.assertEqual(not_updated_category, self.category_1)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_delete_category(self):
    self.assertEqual(Category.objects.count(), 12)
    response = self.client.delete(path=reverse('category', kwargs={'pk': self.category_1.pk}))
    self.assertEqual(Category.objects.count(), 12)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_delete_category_by_name(self):
    self.assertEqual(Category.objects.count(), 12)
    response = self.client.delete(path=reverse('category', kwargs={'name': self.category_1.name}))
    self.assertEqual(Category.objects.count(), 12)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    