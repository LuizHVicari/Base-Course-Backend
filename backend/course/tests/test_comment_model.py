from django.test import TestCase
from django.core.exceptions import ValidationError

from course.models import Comment
from course.factories import CommentFactory, LessonFactory, UserFactory


class TestCommentModel(TestCase):
  def setUp(self):
    self.comment = CommentFactory()

  
  def test_comment_str(self):
    self.assertEqual(str(self.comment), f'{self.comment.user.username}{self.comment.text}')

  
  def test_can_create_comment_with_lesson(self):
    comment = Comment(
      user=self.comment.user,
      lesson=self.comment.lesson,
      text='This is a comment',
      stars=5
    )
    comment.full_clean()
    comment.save()

    self.assertEqual(comment.user, self.comment.user)
    self.assertEqual(comment.lesson, self.comment.lesson)
    self.assertEqual(comment.text, 'This is a comment')
    self.assertEqual(comment.stars, 5)
    self.assertEqual(Comment.objects.count(), 2)

  
  def test_can_create_comment_with_comment(self):
    comment = Comment(
      user=self.comment.user,
      comment_fk=self.comment,
      text='This is a comment',
      stars=5
    )
    comment.full_clean()
    comment.save()

    self.assertEqual(comment.user, self.comment.user)
    self.assertEqual(comment.comment_fk, self.comment)
    self.assertEqual(comment.text, 'This is a comment')
    self.assertEqual(comment.stars, 5)
    self.assertEqual(Comment.objects.count(), 2)

  
  def test_cant_create_comment_without_parent_or_lesson(self):
    with self.assertRaises(ValidationError):
      comment = Comment(
        user=self.comment.user,
        text='This is a comment',
        stars=5
      )
      comment.full_clean()
      comment.save()


  def test_cant_create_comment_with_both_parent_and_lesson(self):
    with self.assertRaises(ValidationError):
      comment = Comment(
        user=self.comment.user,
        lesson=self.comment.lesson,
        comment_fk=self.comment,
        text='This is a comment',
        stars=5
      )
      comment.full_clean()
      comment.save()


  def test_cant_create_comment_without_user(self):
    with self.assertRaises(ValidationError):
      comment = Comment(
        text='This is a comment',
        stars=5,
        comment_fk=self.comment
      )
      comment.full_clean()
      comment.save()

  
  def test_can_create_comment_without_text(self):
    comment = Comment(
      user=self.comment.user,
      stars=5,
      comment_fk=self.comment
    )
    comment.full_clean()
    comment.save()

    self.assertEqual(comment.user, self.comment.user)
    self.assertEqual(comment.stars, 5)
    self.assertEqual(Comment.objects.count(), 2)
    self.assertEqual(comment.text, None)

  
  def test_cant_create_comment_with_more_than_5_stars(self):
    with self.assertRaises(ValidationError):
      comment = Comment(
        user=self.comment.user,
        text='This is a comment',
        stars=6,
        comment_fk=self.comment
      )
      comment.full_clean()
      comment.save()


  def test_cant_create_comment_with_less_than_0_stars(self):
    with self.assertRaises(ValidationError):
      comment = Comment(
        user=self.comment.user,
        text='This is a comment',
        stars=-1,
        comment_fk=self.comment
      )
      comment.full_clean()
      comment.save()

  
  def test_can_create_comment_with_no_stars(self):
    comment = Comment(
      user=self.comment.user,
      text='This is a comment',
      comment_fk=self.comment
    )
    comment.full_clean()
    comment.save()

    self.assertEqual(comment.user, self.comment.user)
    self.assertEqual(comment.text, 'This is a comment')
    self.assertEqual(comment.stars, None)
    self.assertEqual(Comment.objects.count(), 2)