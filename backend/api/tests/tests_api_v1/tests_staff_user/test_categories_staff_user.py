from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import CategoryFactory, UserFactory
from course.models import Category
from api.serializers import CategorySerializerV1
from backend.faker_base import faker


class TestStaffUserCategory(APITestCase):
  def setUp(self):
    faker.unique.clear()
    self.category_1 = CategoryFactory()
    self.category_2 = CategoryFactory()

    for _ in range(10):
      CategoryFactory()

    self.user = UserFactory()
    self.user.is_staff = True
    self.user.save()
    
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)
    self.client.credentials(HTTP_ACCEPT='application/json; version=v1')

    self.only_fields = 'id', 'name', 'description', 'color', 'created_at', 'updated_at'


  def assert_data_is_equal(self, response, serializer):
    self.assertEqual(response.data['id'], serializer.data['id'])
    self.assertEqual(response.data['name'], serializer.data['name'])
    self.assertEqual(response.data['description'], serializer.data['description'])
    self.assertEqual(response.data['color'], serializer.data['color'])
    self.assertEqual(response.data['created_at'], serializer.data['created_at'])
    self.assertEqual(response.data['updated_at'], serializer.data['updated_at'])

  
  def test_staff_user_can_list_all_cateogries(self):
    response = self.client.get(path=reverse('categories'))
    categories = Category.objects.all().only(*self.only_fields)
    serializer = CategorySerializerV1(categories, many=True)
    
    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_staff_user_can_post_category(self):
    response = self.client.post(
      path=reverse('categories'), 
      data={
        'name': 'new category',
        'description': 'new category description',
        'color': '#000000'})
    self.assertEqual(Category.objects.count(), 13)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  
  def test_staff_user_can_list_all_categories_by_name(self):
    response = self.client.get(
      path=reverse('categories',
      kwargs={'name': self.category_1.name}))
    categories = Category.objects.filter(name__icontains=self.category_1.name).only(*self.only_fields)
    serializer = CategorySerializerV1(categories, many=True)
    
    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_staff_user_can_retrieve_any_category(self):
    response = self.client.get(
      path=reverse('category', args=[self.category_1.id]))
    category = Category.objects.get(pk=self.category_1.id)
    serializer = CategorySerializerV1(category)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, serializer.data)

  
  def test_staff_user_can_update_any_category(self):
    response = self.client.put(
      path=reverse('category', args=[self.category_1.id]),
      data={
        'name': 'updated category',
        'description': 'updated category description',
        'color': '#000000'})
    category = Category.objects.get(pk=self.category_1.id)
    serializer = CategorySerializerV1(category)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)

  
  def test_staff_user_can_patch_any_category(self):
    response = self.client.patch(
      path=reverse('category', args=[self.category_1.id]),
      data={
        'name': 'updated category'})
    category = Category.objects.get(pk=self.category_1.id)
    serializer = CategorySerializerV1(category)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)

  
  def test_staff_user_can_delete_any_category(self):
    response = self.client.delete(
      path=reverse('category', args=[self.category_1.id]))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Category.objects.count(), 11)

  
  def test_staff_user_can_retrieve_any_category_by_name(self):
    response = self.client.get(
      path=reverse('category', kwargs={'name': self.category_1.name}))
    category = Category.objects.get(name=self.category_1.name)
    serializer = CategorySerializerV1(category)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, serializer.data)

  
  def test_staff_user_can_update_any_category_by_name(self):
    response = self.client.put(
      path=reverse('category', kwargs={'name': self.category_1.name}),
      data={
        'name': 'updated category',
        'description': 'updated category description',
        'color': '#000000'})
    category = Category.objects.get(pk=self.category_1.id)
    serializer = CategorySerializerV1(category)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)

  
  def test_staff_user_can_patch_any_category_by_name(self):
    response = self.client.patch(
      path=reverse('category', kwargs={'name': self.category_1.name}),
      data={
        'name': 'updated category'})
    category = Category.objects.get(pk=self.category_1.id)
    serializer = CategorySerializerV1(category)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)


  def test_staff_user_can_delete_any_category_by_name(self):
    response = self.client.delete(
      path=reverse('category', kwargs={'name': self.category_1.name}))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Category.objects.count(), 11)

  
  def test_staff_user_cannot_retrieve_category_that_does_not_exist(self):
    response = self.client.get(path=reverse('category', args=[999]))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_staff_user_cannot_retreive_category_by_name_that_does_not_exist(self):
    response = self.client.get(
      path=reverse('category', kwargs={'name': 'non-existent category'}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)