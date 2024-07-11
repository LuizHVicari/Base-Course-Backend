from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import LessonFactory
from course.models import Lesson
from api.serializers import LessonSerializerV1
from backend.faker_base import faker


class TestAnonUserLessons(APITestCase):
  def setUp(self):
    self.lesson_1 = LessonFactory()
    self.lesson_2 = LessonFactory()
    for _ in range(10):
      LessonFactory()

    self.client = APIClient()

  def compare_results(self, response, serializer):
    results = response.data.get('results')
    if results == None:
      response.data['cover'] = response.data['cover'].removeprefix('http://testserver')
      response.data['video'] = response.data['video'].removeprefix('http://testserver')
      self.assertEqual(response.data, serializer.data)
      return 
    
    for item in results:
      item['cover'] = item['cover'].removeprefix('http://testserver')
      item['video'] = item['video'].removeprefix('http://testserver')
      
    self.assertCountEqual(response.data.get('results'), serializer.data)
    return 

  
  def test_anon_user_can_list_all_lessons(self):
    response = self.client.get(path=reverse('lessons'))
    lessons = Lesson.objects.all()
    serializer = LessonSerializerV1(lessons, many=True)
    
    self.compare_results(response, serializer)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_can_filter_lessons_by_course(self):
    response = self.client.get(
      path=reverse('lessons'), 
      QUERY_STRING=f'course={self.lesson_1.course.title}')
    lessons = Lesson.objects.filter(course__title__icontains=self.lesson_1.course.title)
    serializer = LessonSerializerV1(lessons, many=True)

    self.compare_results(response, serializer)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_can_filter_lessons_by_title(self):
    response = self.client.get(
      path=reverse('lessons'), 
      QUERY_STRING=f'title={self.lesson_1.title}')
    lessons = Lesson.objects.filter(title__icontains=self.lesson_1.title)
    serializer = LessonSerializerV1(lessons, many=True)

    self.compare_results(response, serializer)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_can_filter_lessons_by_author(self):
    response = self.client.get(
      path=reverse('lessons'), 
      QUERY_STRING=f'author={self.lesson_1.author.username}')
    lessons = Lesson.objects.filter(author__username__icontains=self.lesson_1.author.username)
    serializer = LessonSerializerV1(lessons, many=True)

    self.compare_results(response, serializer)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_can_filter_lessons_by_course_and_title_and_author(self):
    response = self.client.get(
      path=reverse('lessons'), 
      QUERY_STRING=f'course={self.lesson_1.course.title}&title={self.lesson_1.title}&author={self.lesson_1.author.username}')
    lessons = Lesson.objects.filter(
      course__title__icontains=self.lesson_1.course.title,
      title__icontains=self.lesson_1.title,
      author__username__icontains=self.lesson_1.author.username)
    serializer = LessonSerializerV1(lessons, many=True)

    self.compare_results(response, serializer)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_cannot_post_to_lessons(self):
    response = self.client.post(path=reverse('lessons'), data={
      'title': faker.unique.word(),
      'description': faker.sentence(),
      'course': self.lesson_1.course.pk,
      'cover': faker.image_url(),
      'video': faker.file_path(),
      'text': faker.paragraph(),
      'author': self.lesson_1.author.pk
    })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_can_retrieve_any_lesson(self):
    response = self.client.get(path=reverse('lesson', kwargs={'pk': self.lesson_1.pk}))
    lesson = Lesson.objects.get(pk=self.lesson_1.pk)
    serializer = LessonSerializerV1(lesson)

    self.compare_results(response, serializer)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_cannot_retrieve_non_existent_lesson(self):
    response = self.client.get(path=reverse('lesson', kwargs={'pk': 999}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_anon_user_can_retrieve_any_lesson_by_title(self):
    response = self.client.get(path=reverse('lesson', kwargs={'title': self.lesson_1.title}))
    lesson = Lesson.objects.get(title=self.lesson_1.title)
    serializer = LessonSerializerV1(lesson)

    self.compare_results(response, serializer)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_cannot_retrieve_non_existent_lesson_by_title(self):
    response = self.client.get(path=reverse('lesson', kwargs={'title': faker.unique.word()}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_anon_user_cannot_put_to_lessons(self):
    response = self.client.put(path=reverse('lesson', kwargs={'pk': self.lesson_1.pk}), data={
      'title': faker.unique.word(),
      'description': faker.sentence(),
      'course': self.lesson_1.course.pk,
      'cover': faker.image_url(),
      'video': faker.file_path(),
      'text': faker.paragraph(),
      'author': self.lesson_1.author.pk
    })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_put_to_lessons_by_title(self):
    response = self.client.put(path=reverse('lesson', kwargs={'title': self.lesson_1.title}), data={
      'title': faker.unique.word(),
      'description': faker.sentence(),
      'course': self.lesson_1.course.pk,
      'cover': faker.image_url(),
      'video': faker.file_path(),
      'text': faker.paragraph(),
      'author': self.lesson_1.author.pk
    })
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_patch_to_lessons(self):
    response = self.client.patch(path=reverse('lesson', kwargs={'pk': self.lesson_1.pk}), data={'title': faker.unique.word()})
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_patch_to_lessons_by_title(self):
    response = self.client.patch(path=reverse('lesson', kwargs={'title': self.lesson_1.title}), data={'title': faker.unique.word()})
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_delete_lessons(self):
    response = self.client.delete(path=reverse('lesson', kwargs={'pk': self.lesson_1.pk}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_delete_lessons_by_title(self):
    response = self.client.delete(path=reverse('lesson', kwargs={'title': self.lesson_1.title}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


  
  