from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.db.models import Count

from course.factories import CourseFactory, LessonFactory, UserFactory
from course.models import Course
from api.serializers import CourseSerializerV1
from backend.faker_base import faker


class TestStaffUserCategories(APITestCase):
  def setUp(self):
    faker.unique.clear()
    self.course_1 = CourseFactory()
    self.course_2 = CourseFactory()
    for _ in range(10):
      CourseFactory()
    
    for _ in range(10):
      LessonFactory(course=self.course_1)
    for _ in range(5):
      LessonFactory(course=self.course_2)

    self.user = UserFactory()
    self.user.is_staff = True
    self.user.save()

    self.client = APIClient()
    self.client.force_authenticate(user=self.user)
    self.client.credentials(HTTP_ACCEPT='application/json; version=v1')

    self.only_fields = 'id', 'title', 'description', 'cover', 'created_at', 'updated_at'
    

  def compare_results(self, response, serializer):
    results = response.data.get('results')
    if results == None:
      response.data['cover'] = response.data['cover'].removeprefix('http://testserver')
      self.assertEqual(response.data, serializer.data)
      return 
    
    for item in results:
      item['cover'] = item['cover'].removeprefix('http://testserver')
    self.assertCountEqual(response.data.get('results'), serializer.data)
    return 
  
  
  def assert_data_is_equal(self, response, serializer):
    self.assertEqual(response.data['id'], serializer.data['id'])
    self.assertEqual(response.data['title'], serializer.data['title'])
    self.assertEqual(response.data['description'], serializer.data['description'])
    self.assertEqual(response.data['cover'].removeprefix('http://testserver'), serializer.data['cover'])
    self.assertEqual(response.data['created_at'], serializer.data['created_at'])
    self.assertEqual(response.data['updated_at'], serializer.data['updated_at'])


  def test_staff_user_can_list_all_courses(self):
    response = self.client.get(path=reverse('courses'))
    courses = Course.objects.all().only(*self.only_fields)
    serializer = CourseSerializerV1(courses, many=True)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_staff_user_can_post_course(self):
    response = self.client.post(
      path=reverse('courses'), 
      data={
        'title': 'new course',
        'category': self.course_1.category.id,
        'description': 'new course description',
        'cover': self.course_1.cover,})
    self.assertEqual(Course.objects.count(), 13)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  
  def test_staff_user_can_list_all_courses_by_all_fields(self):
    response = self.client.get(
      path=reverse('courses'), 
      QUERY_STRING=f'title={self.course_1.title}' +
                   f'&category={self.course_1.category.name}' +
                   f'&max_lessons={self.course_1.lesson_set.count()}' +
                   f'&min_lessons={self.course_1.lesson_set.count()}')
    courses = Course.objects.filter(
      title__icontains=self.course_1.title,
      category__name__icontains=self.course_1.category.name).annotate(
        lesson_count=Count('lesson')).filter(
          lesson_count__lte=self.course_1.lesson_set.count(),
          lesson_count__gte=self.course_1.lesson_set.count()).only(*self.only_fields)
    serializer = CourseSerializerV1(courses, many=True)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_staff_user_can_retrieve_any_course(self):
    response = self.client.get(
      path=reverse('course', args=[self.course_1.id]))
    course = Course.objects.get(pk=self.course_1.id)
    serializer = CourseSerializerV1(course)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_staff_user_cannot_retrieve_a_course_that_does_not_exist(self):
    response = self.client.get(
      path=reverse('course', args=[999]))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_staff_user_can_put_any_course(self):
    response = self.client.put(
      path=reverse('course', args=[self.course_1.id]),
      data={
        'title': 'updated course',
        'category': self.course_1.category.id,
        'description': 'updated course description',
        'cover': self.course_1.cover})
    course = Course.objects.get(pk=self.course_1.id)
    serializer = CourseSerializerV1(course)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)
    self.assertEqual(response.data['title'], 'updated course')

  
  def test_staff_user_can_patch_any_course(self):
    response = self.client.patch(
      path=reverse('course', args=[self.course_1.id]),
      data={'title': 'updated course'})
    course = Course.objects.get(pk=self.course_1.id)
    serializer = CourseSerializerV1(course)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)
    self.assertEqual(response.data['title'], 'updated course')

  
  def test_staff_user_can_delete_any_course(self):
    response = self.client.delete(
      path=reverse('course', args=[self.course_1.id]))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Course.objects.count(), 11)

  
  def test_staff_user_can_retrieve_any_course_by_title(self):
    response = self.client.get(
      path=reverse('course', kwargs={'title': self.course_1.title}))
    course = Course.objects.get(title=self.course_1.title)
    serializer = CourseSerializerV1(course)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_staff_user_cannot_retrieve_course_that_does_not_exist(self):
    response = self.client.get(
      path=reverse('course', kwargs={'title': 'non-existent course'}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_staff_user_can_update_any_course_by_title(self):
    response = self.client.put(
      path=reverse('course', kwargs={'title': self.course_1.title}),
      data={
        'title': 'updated course',
        'category': self.course_1.category.id,
        'description': 'updated course description',
        'cover': self.course_1.cover})
    course = Course.objects.get(pk=self.course_1.id)
    serializer = CourseSerializerV1(course)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)
    self.assertEqual(response.data['title'], 'updated course')

  
  def test_staff_user_can_patch_any_course_by_title(self):
    response = self.client.patch(
      path=reverse('course', kwargs={'title': self.course_1.title}),
      data={'title': 'updated course'})
    course = Course.objects.get(pk=self.course_1.id)
    serializer = CourseSerializerV1(course)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)
    self.assertEqual(response.data['title'], 'updated course')

  
  def test_staff_user_can_delete_any_course_by_title(self):
    response = self.client.delete(
      path=reverse('course', kwargs={'title': self.course_1.title}))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Course.objects.count(), 11)
  