from django.test import TestCase
from django.core.exceptions import ValidationError

from course.factories import SaveFactory, LessonFactory
from course.models import Save


class TestSaveModel(TestCase):
  def setUp(self):
    self.save = SaveFactory()

  
  def test_save_str(self):
    self.assertEqual(str(self.save), f'{self.save.user.username} - {self.save.lesson.title}')


  def test_can_create_save(self):
    new_lesson = LessonFactory()
    new_save = Save(
      user=self.save.user,
      lesson=new_lesson
    )
    new_save.full_clean()
    new_save.save()
    self.assertEqual(Save.objects.count(), 2)

  
  def test_can_delete_save(self):
    self.save.delete()
    self.assertEqual(Save.objects.count(), 0)

  
  def test_can_update_save(self):
    updated_date = self.save.updated_at
    self.save.lesson = LessonFactory()
    self.save.full_clean()
    self.save.save()
    self.assertNotEqual(self.save.updated_at, updated_date)


  def test_cant_create_duplicate_save(self):
    new_save = Save(
      user=self.save.user,
      lesson=self.save.lesson
    )
    with self.assertRaises(ValidationError):
      new_save.full_clean()
      new_save.save()
    self.assertEqual(Save.objects.count(), 1)

  
  def test_cant_create_save_with_no_lesson(self):
    new_save = Save(
      user=self.save.user
    )
    with self.assertRaises(ValidationError):
      new_save.full_clean()
      new_save.save()
    self.assertEqual(Save.objects.count(), 1)

  
  def test_cant_create_save_with_no_user(self):
    new_lesson = LessonFactory()
    new_save = Save(
      lesson=new_lesson
    )
    with self.assertRaises(ValidationError):
      new_save.full_clean()
      new_save.save()
    self.assertEqual(Save.objects.count(), 1)