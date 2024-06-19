from django.test import TestCase
from django.core.exceptions import ValidationError

from course.models import Watched
from course.factories import WatchedFactory, LessonFactory, UserFactory


class TestWatchedModel(TestCase):
  def setUp(self):
    self.watched = WatchedFactory()

  
  def test_watched_str(self):
    self.assertEqual(str(self.watched), f'{self.watched.user.username} - {self.watched.lesson.title}')

  
  def test_can_create_watched(self):
    user = UserFactory()
    lesson = LessonFactory()
    watched = Watched(
      user=user,
      lesson=lesson,
      watched_time=50
    )
    watched.full_clean()
    watched.save()

    self.assertEqual(watched.user, user)
    self.assertEqual(watched.lesson, lesson)
    self.assertEqual(watched.watched_time, 50)
    self.assertEqual(Watched.objects.count(), 2)

  
  def test_can_update_watched_time(self):
    watched = WatchedFactory()
    updated_date = watched.updated_at
    watched.watched_time = 100

    watched.full_clean()
    watched.save()

    self.assertEqual(watched.watched_time, 100)
    self.assertNotEqual(watched.updated_at, updated_date)

  
  def test_can_delete_watched(self):
    watched = WatchedFactory()
    watched.delete()
    self.assertEqual(Watched.objects.count(), 1)

  
  def test_cant_create_duplicate_watched(self):
    watched = Watched(
      user=self.watched.user,
      lesson=self.watched.lesson
    )
    with self.assertRaises(ValidationError):
      watched.full_clean()
      watched.save()
    self.assertEqual(Watched.objects.count(), 1)

  
  def test_cant_create_watched_with_no_lesson(self):
    watched = Watched(
      user=self.watched.user
    )
    with self.assertRaises(ValidationError):
      watched.full_clean()
      watched.save()
    self.assertEqual(Watched.objects.count(), 1)

  
  def test_cant_create_watched_with_no_user(self):
    watched = Watched(
      lesson=self.watched.lesson
    )
    with self.assertRaises(ValidationError):
      watched.full_clean()
      watched.save()
    self.assertEqual(Watched.objects.count(), 1)