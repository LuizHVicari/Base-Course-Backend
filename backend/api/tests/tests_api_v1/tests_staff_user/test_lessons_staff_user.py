from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from course.factories import LessonFactory, UserFactory
from course.models import Lesson
from api.serializers import LessonSerializerV1
from backend.faker_base import faker


class TestStaffUserLessons(APITestCase):
  def setUp(self):
    faker.unique.clear()
    self.lesson_1 = LessonFactory()
    self.lesson_2 = LessonFactory()
    for _ in range(10):
      LessonFactory()

    self.user = UserFactory()
    self.user.is_staff = True
    self.user.save()

    self.client = APIClient()
    self.client.force_authenticate(user=self.user)
    self.client.credentials(HTTP_ACCEPT='application/json; version=v1')

    self.only_fields = 'id', 'title', 'description', 'cover', 'video', 'text', 'author', 'course', 'created_at', 'updated_at'


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
  
  
  def assert_data_is_equal(self, response, serializer):
    self.assertEqual(response.data['id'], serializer.data['id'])
    self.assertEqual(response.data['title'], serializer.data['title'])
    self.assertEqual(response.data['description'], serializer.data['description'])
    self.assertEqual(response.data['cover'].removeprefix('http://testserver'), serializer.data['cover'])
    self.assertEqual(response.data['video'].removeprefix('http://testserver'), serializer.data['video'])
    self.assertEqual(response.data['text'], serializer.data['text'])
    self.assertEqual(response.data['author'], serializer.data['author'])
    self.assertEqual(response.data['course'], serializer.data['course'])
    self.assertEqual(response.data['created_at'], serializer.data['created_at'])
    self.assertEqual(response.data['updated_at'], serializer.data['updated_at'])

  
  def test_staff_user_can_list_all_lessons(self):
    response = self.client.get(path=reverse('lessons'))
    lessons = Lesson.objects.all().only(*self.only_fields)
    serializer = LessonSerializerV1(lessons, many=True)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_staff_user_can_post_lesson(self):
    response = self.client.post(
      path=reverse('lessons'), 
      data={
        'title': 'new lesson',
        'description': 'new lesson description',
        'cover': self.lesson_1.cover,
        'video': SimpleUploadedFile('video.mp4', b'file_content', content_type='video/mp4'),
        'text': 'new lesson text',
        'author': 1,
        'course': 1})
    self.assertEqual(Lesson.objects.count(), 13)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  
  def test_staff_user_can_list_all_lessons_by_all_fields(self):
    response = self.client.get(
      path=reverse('lessons'), 
      QUERY_STRING=f'course={self.lesson_1.course.title}' +
                   f'&title={self.lesson_1.title}' +
                   f'&author={self.lesson_1.author}')
    lessons = Lesson.objects.filter(
      title=self.lesson_1.title,
      description=self.lesson_1.description,
      author=self.lesson_1.author,
      course=self.lesson_1.course).only(*self.only_fields)
    serializer = LessonSerializerV1(lessons, many=True)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.compare_results(response, serializer)

  
  def test_staff_user_can_retrieve_any_lesson(self):
    response = self.client.get(
      path=reverse('lesson', args=[self.lesson_1.id]))
    lesson = Lesson.objects.get(pk=self.lesson_1.id)
    serializer = LessonSerializerV1(lesson)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)

  
  def test_staff_user_cannot_retrieve_any_lesson_with_invalid_id(self):
    response = self.client.get(
      path=reverse('lesson', args=[1000]))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_staff_user_can_update_any_lesson(self):
    response = self.client.put(
      path=reverse('lesson', args=[self.lesson_1.id]),
      data={
        'title': 'updated lesson',
        'description': 'updated lesson description',
        'cover': self.lesson_1.cover,
        'video': SimpleUploadedFile('video.mp4', b'file_content', content_type='video/mp4'),
        'text': 'updated lesson text',
        'author': 1,
        'course': 1})
    lesson = Lesson.objects.get(pk=self.lesson_1.id)
    serializer = LessonSerializerV1(lesson)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)
    self.assertEqual(response.data['title'], 'updated lesson')

  
  def test_staff_user_can_patch_any_lesson(self):
    response = self.client.patch(
      path=reverse('lesson', args=[self.lesson_1.id]),
      data={
        'title': 'updated lesson'})
    lesson = Lesson.objects.get(pk=self.lesson_1.id)
    serializer = LessonSerializerV1(lesson)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)
    self.assertEqual(response.data['title'], 'updated lesson')

  
  def test_staff_user_can_delete_any_lesson(self):
    response = self.client.delete(
      path=reverse('lesson', args=[self.lesson_1.id]))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Lesson.objects.count(), 11)


  def test_staff_user_can_retrieve_any_lesson_by_title(self):
    response = self.client.get(
      path=reverse('lesson', kwargs={'title': self.lesson_1.title}))
    lesson = Lesson.objects.get(title=self.lesson_1.title)
    serializer = LessonSerializerV1(lesson)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)

  
  def test_staff_user_cannot_retrieve_lesson_by_title_that_does_not_exist(self):
    response = self.client.get(
      path=reverse('lesson', kwargs={'title': 'lesson that does not exist'}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_staff_user_can_update_any_lesson_by_title(self):
    response = self.client.put(
      path=reverse('lesson', kwargs={'title': self.lesson_1.title}),
      data={
        'title': 'updated lesson',
        'description': 'updated lesson description',
        'cover': self.lesson_1.cover,
        'video': SimpleUploadedFile('video.mp4', b'file_content', content_type='video/mp4'),
        'text': 'updated lesson text',
        'author': 1,
        'course': 1})
    lesson = Lesson.objects.get(pk=self.lesson_1.id)
    serializer = LessonSerializerV1(lesson)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)
    self.assertEqual(response.data['title'], 'updated lesson')

  
  def test_staff_user_can_patch_any_lesson_by_title(self):
    response = self.client.patch(
      path=reverse('lesson', kwargs={'title': self.lesson_1.title}),
      data={
        'title': 'updated lesson'})
    lesson = Lesson.objects.get(pk=self.lesson_1.id)
    serializer = LessonSerializerV1(lesson)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)
    self.assertEqual(response.data['title'], 'updated lesson')

  
  def test_staff_user_can_delete_any_lesson_by_title(self):
    response = self.client.delete(
      path=reverse('lesson', kwargs={'title': self.lesson_1.title}))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Lesson.objects.count(), 11)