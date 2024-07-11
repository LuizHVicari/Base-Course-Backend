from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import CommentFactory
from course.models import Comment
from api.serializers import CommentSerializerV1
from backend.faker_base import faker


class TestAnonUserComments(APITestCase):
  def setUp(self):
    self.comments_1 = CommentFactory()
    self.comments_2 = CommentFactory()
    for _ in range(10):
      CommentFactory()

    self.client = APIClient()

  
  def test_anon_user_can_list_all_comments(self):
    response = self.client.get(path=reverse('comments'))
    comments = Comment.objects.all()
    serializer = CommentSerializerV1(comments, many=True)
    
    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_can_filter_comments_by_user(self):
    response = self.client.get(
      path=reverse('comments'), 
      QUERY_STRING=f'user={self.comments_1.user.username}')
    comments = Comment.objects.filter(user__username__icontains=self.comments_1.user.username)
    serializer = CommentSerializerV1(comments, many=True)

    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_can_filter_comments_by_lesson(self):
    response = self.client.get(
      path=reverse('comments'), 
      QUERY_STRING=f'lesson={self.comments_1.lesson.title}')
    comments = Comment.objects.filter(lesson__title__icontains=self.comments_1.lesson.title)
    serializer = CommentSerializerV1(comments, many=True)

    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)


  def test_anon_user_cannot_filter_comments_by_stars_with_no_lesson(self):
    response = self.client.get(
      path=reverse('comments'), 
      QUERY_STRING=f'stars={self.comments_1.stars}')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  
  def test_anon_user_can_filter_comments_by_user_lesson_and_stars(self):
    response = self.client.get(
      path=reverse('comments'), 
      QUERY_STRING=f'user={self.comments_1.user.username}&lesson={self.comments_1.lesson.title}&stars={self.comments_1.stars}')
    comments = Comment.objects.filter(
      user__username__icontains=self.comments_1.user.username,
      lesson__title__icontains=self.comments_1.lesson.title,
      stars=self.comments_1.stars)
    serializer = CommentSerializerV1(comments, many=True)

    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_cannot_post_to_comments(self):
    response = self.client.post(path=reverse('comments'), data={
      'user': self.comments_1.user.pk,
      'lesson': self.comments_1.lesson.pk,
      'stars': self.comments_1.stars,
      'comment': faker.paragraph()
    })

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_can_retrieve_any_comment(self):
    response = self.client.get(path=reverse('comment', kwargs={'pk': self.comments_1.pk}))
    comment = Comment.objects.get(pk=self.comments_1.pk)
    serializer = CommentSerializerV1(comment)

    self.assertEqual(response.data, serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_anon_user_cannot_retrieve_non_existent_comment(self):
    response = self.client.get(path=reverse('comment', kwargs={'pk': 999}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_anon_user_cannot_put_to_comments(self):
    response = self.client.put(
      path=reverse('comment', kwargs={'pk': self.comments_1.pk}), 
      data={
        'user': self.comments_1.user.pk,
        'lesson': self.comments_1.lesson.pk,
        'stars': self.comments_1.stars,
        'comment': faker.paragraph()
      })

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  
  def test_anon_user_cannot_delete_comments(self):
    response = self.client.delete(path=reverse('comment', kwargs={'pk': self.comments_1.pk}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertTrue(Comment.objects.filter(pk=self.comments_1.pk).exists())
  
  