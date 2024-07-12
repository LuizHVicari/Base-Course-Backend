from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.db.models import Count

from course.factories import CourseFactory, LessonFactory
from course.models import Course
from api.serializers import CourseSerializerV1
from backend.faker_base import faker


class TestAnonUserCategories(APITestCase):
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

    self.client = APIClient()
    self.client.credentials(HTTP_ACCEPT='application/json; version=v1')
    

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


  def test_anon_user_can_list_all_courses(self):
    response = self.client.get(path=reverse('courses'))
    courses = Course.objects.all()
    serializer = CourseSerializerV1(courses, many=True)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_anon_user_can_list_courses_by_title(self):
    response = self.client.get(
      path=reverse('courses'), 
      QUERY_STRING=f'title={self.course_1.title}')
    courses = Course.objects.filter(title=self.course_1.title)
    serializer = CourseSerializerV1(courses, many=True)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_anon_user_can_list_courses_by_partial_title(self):
    response = self.client.get(
      path=reverse('courses'), 
      QUERY_STRING=f'title={self.course_1.title[:3]}')
    courses = Course.objects.filter(title__icontains=self.course_1.title[:3])
    serializer = CourseSerializerV1(courses, many=True)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_anon_user_can_list_courses_by_category(self):
    response = self.client.get(
      path=reverse('courses'), 
      QUERY_STRING=f'category={self.course_1.category.name}')
    courses = Course.objects.filter(category__name=self.course_1.category)
    serializer = CourseSerializerV1(courses, many=True)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_anon_user_can_list_courses_by_partial_category(self):
    response = self.client.get(
      path=reverse('courses'), 
      QUERY_STRING=f'category={self.course_1.category.name[:3]}')
    courses = Course.objects.filter(
      category__name__icontains=self.course_1.category.name[:3])
    serializer = CourseSerializerV1(courses, many=True)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_anon_user_can_list_courses_by_max_lessons(self):
    response = self.client.get(
      path=reverse('courses'),
      QUERY_STRING=f'max_lessons={self.course_1.lesson_set.count()}')
    courses = Course.objects.annotate(
      lesson_count=Count('lesson')).filter(
        lesson_count__lte=self.course_1.lesson_set.count())
    serializer = CourseSerializerV1(courses, many=True)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_anon_user_can_list_courses_by_min_lessons(self):
    response = self.client.get(
      path=reverse('courses'), 
      QUERY_STRING=f'min_lessons={self.course_1.lesson_set.count()}')
    courses = Course.objects.annotate(
      lesson_count=Count('lesson')).filter(
        lesson_count__gte=self.course_1.lesson_set.count())
    serializer = CourseSerializerV1(courses, many=True)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_anon_user_can_courses_by_full_filter_url(self):
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
          lesson_count__gte=self.course_1.lesson_set.count())
    serializer = CourseSerializerV1(courses, many=True)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_anon_user_cannot_post_to_courses(self):
    self.assertEqual(Course.objects.count(), 12)
    response = self.client.post(path=reverse('courses'), data={
      'title': faker.unique.word(),
      'description': faker.sentence(),
      'category': self.course_1.category.pk,
      'cover': faker.image_url(),
    })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
  

  def test_anon_user_can_retrieve_any_course(self):
    response = self.client.get(path=reverse('course', kwargs={'pk': self.course_1.pk}))
    course = Course.objects.get(pk=self.course_1.pk)
    serializer = CourseSerializerV1(course)

    self.compare_results(response, serializer)
    self.assertEqual(response.data, serializer.data)
  

  def test_anon_user_cannot_retrieve_non_existent_course(self):
    response = self.client.get(path=reverse('course', kwargs={'pk': 999}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


  def test_anon_user_can_retrieve_any_course_by_title(self):
    response = self.client.get(path=reverse('course', kwargs={'title': self.course_1.title}))
    course = Course.objects.get(title=self.course_1.title)
    serializer = CourseSerializerV1(course)

    self.compare_results(response, serializer)
    self.assertEqual(response.data, serializer.data)


  def test_anon_user_cannot_put_to_course(self):
    course = Course.objects.get(pk=self.course_1.pk)
    response = self.client.put(path=reverse(
      'course', 
      kwargs={'pk': self.course_1.pk}), 
      data={
        'title': faker.unique.word(),
        'description': faker.sentence(),
        'category': self.course_1.category.pk,
        'cover': faker.image_url(),
    })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(Course.objects.get(pk=self.course_1.pk), course)


  def test_anon_user_cannot_put_to_course_by_title(self):
    course = Course.objects.get(title=self.course_1.title)
    response = self.client.put(path=reverse(
      'course', 
      kwargs={'title': self.course_1.title}), 
      data={
        'title': faker.unique.word(),
        'description': faker.sentence(),
        'category': self.course_1.category.pk,
        'cover': faker.image_url(),
    })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(Course.objects.get(title=self.course_1.title), course)


  def test_anon_user_cant_patch_to_course(self):
    course = Course.objects.get(pk=self.course_1.pk)
    response = self.client.patch(path=reverse(
      'course', 
      kwargs={'pk': self.course_1.pk}), 
      data={'title': faker.unique.word()})
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(Course.objects.get(pk=self.course_1.pk), course)

  
  def test_anon_user_cannot_patch_to_course_by_title(self):
    course = Course.objects.get(title=self.course_1.title)
    response = self.client.patch(path=reverse(
      'course', 
      kwargs={'title': self.course_1.title}), 
      data={'title': faker.unique.word()})
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(Course.objects.get(title=self.course_1.title), course)


  def test_anon_user_cannot_delete_course(self):
    self.assertEqual(Course.objects.count(), 12)
    response = self.client.delete(path=reverse('course', kwargs={'pk': self.course_1.pk}))
    self.assertEqual(Course.objects.count(), 12)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_delete_course_by_title(self):
    self.assertEqual(Course.objects.count(), 12)
    response = self.client.delete(path=reverse('course', kwargs={'title': self.course_1.title}))
    self.assertEqual(Course.objects.count(), 12)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)