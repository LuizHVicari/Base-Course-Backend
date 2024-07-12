from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from course.factories import CommentFactory, UserFactory
from course.models import Comment
from api.serializers import CommentSerializerV1
from backend.faker_base import faker


class TestStaffUserComments(APITestCase):
  def setUp(self):
    faker.unique.clear()
    self.comments_1 = CommentFactory()
    self.comments_2 = CommentFactory()
    for _ in range(10):
      CommentFactory()

    self.user = UserFactory()
    self.user.is_staff = True
    self.user.save()

    self.client = APIClient(user=self.user)
    self.client.force_authenticate(user=self.user)
    self.client.credentials(HTTP_ACCEPT='application/json; version=v1')

  
  def assert_data_is_equal(self, response, serializer):
    self.assertEqual(response.data['id'], serializer.data['id'])
    self.assertEqual(response.data['user'], serializer.data['user'])
    self.assertEqual(response.data['lesson'], serializer.data['lesson'])
    self.assertEqual(response.data['stars'], serializer.data['stars'])
    self.assertEqual(response.data['comment_fk'], serializer.data['comment_fk'])
    self.assertEqual(response.data['created_at'], serializer.data['created_at'])
    self.assertEqual(response.data['updated_at'], serializer.data['updated_at'])

  
  def test_staff_user_can_list_all_comments(self):
    response = self.client.get(path=reverse('comments'))
    comments = Comment.objects.all()
    serializer = CommentSerializerV1(comments, many=True)
    
    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  
  def test_staff_user_can_post_comments(self):
    data = {
      'lesson': self.comments_1.lesson.id,
      'stars': 5,
      'text': faker.paragraph()
    }
    response = self.client.post(path=reverse('comments'), data=data)
    comment = Comment.objects.get(pk=response.data.get('id'))
    serializer = CommentSerializerV1(comment)

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data.get('user'), self.user.id)
    self.assert_data_is_equal(response, serializer)
    self.assertEqual(Comment.objects.count(), 13)

  
  def test_staff_user_can_list_comments_by_all_fields(self):
    response = self.client.get(
      path=reverse('comments'), 
      QUERY_STRING=f'user={self.comments_1.user}&lesson={self.comments_1.lesson}&stars={self.comments_1.stars}')
    comments = Comment.objects.filter(user=self.comments_1.user)
    serializer = CommentSerializerV1(comments, many=True)

    self.assertCountEqual(response.data.get('results'), serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)


  def test_staff_user_can_retrieve_comment(self):
    response = self.client.get(path=reverse('comment', args=[self.comments_1.id]))
    comment = Comment.objects.get(pk=self.comments_1.id)
    serializer = CommentSerializerV1(comment)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)

  
  def test_staff_user_cannot_retrieve_comment_that_does_not_exist(self):
    response = self.client.get(
      path=reverse('comment', args=[1000]))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  
  def test_staff_user_can_update_comment(self):
    response = self.client.put(
      path=reverse('comment', args=[self.comments_1.id]),
      data={
        'lesson': self.comments_1.lesson.id,
        'stars': 5,
        'text': faker.paragraph()})
    comment = Comment.objects.get(pk=self.comments_1.id)
    serializer = CommentSerializerV1(comment)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)
    self.assertEqual(comment.text, response.data['text'])

  
  def test_staff_user_can_patch_comment(self):
    response = self.client.patch(
      path=reverse('comment', args=[self.comments_1.id]),
      data={'text': faker.paragraph()})
    comment = Comment.objects.get(pk=self.comments_1.id)
    serializer = CommentSerializerV1(comment)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assert_data_is_equal(response, serializer)
    self.assertEqual(comment.text, response.data['text'])

  
  def test_staff_user_can_delete_comment(self):
    response = self.client.delete(path=reverse('comment', args=[self.comments_1.id]))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Comment.objects.count(), 11)


  