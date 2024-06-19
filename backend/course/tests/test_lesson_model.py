from django.test import TestCase
from django.core.exceptions import ValidationError

from course.models import Lesson
from course.factories import LessonFactory, CommentFactory, SaveFactory, WatchedFactory


class TestLessonModel(TestCase):
  def setUp(self):
    self.lesson = LessonFactory()

  
  def test_lesson_str(self):
    self.assertEqual(str(self.lesson), self.lesson.title)


  def test_can_create_lesson(self):
    lesson = Lesson(
      title='lesson',
      description='description',
      course=self.lesson.course,
      cover=self.lesson.cover,
      video=self.lesson.video,
      text=self.lesson.text
    )
    lesson.full_clean()
    lesson.save()

    self.assertEqual(lesson.title, 'lesson')
    self.assertEqual(lesson.description, 'description')
    self.assertEqual(lesson.course, self.lesson.course)
    self.assertEqual(lesson.cover, self.lesson.cover)
    self.assertEqual(lesson.video, self.lesson.video)
    self.assertEqual(lesson.text, self.lesson.text)
    self.assertEqual(Lesson.objects.count(), 2)

  
  def test_can_update_lesson(self):
    lesson = LessonFactory()
    updated_date = lesson.updated_at
    lesson.title = 'new title'
    lesson.description = 'new description'
    lesson.course = self.lesson.course
    lesson.cover = self.lesson.cover
    lesson.video = self.lesson.video
    lesson.text = self.lesson.text

    lesson.full_clean()
    lesson.save()

    self.assertEqual(lesson.title, 'new title')
    self.assertEqual(lesson.description, 'new description')
    self.assertEqual(lesson.course, self.lesson.course)
    self.assertEqual(lesson.cover, self.lesson.cover)
    self.assertEqual(lesson.video, self.lesson.video)
    self.assertEqual(lesson.text, self.lesson.text)
    self.assertNotEqual(lesson.updated_at, updated_date)

  
  def test_can_delete_lesson(self):
    lesson = LessonFactory()
    self.assertAlmostEqual(Lesson.objects.count(), 2)

    lesson.delete()

    self.assertEqual(Lesson.objects.count(), 1)
    self.assertNotIn(lesson, Lesson.objects.all())


  def test_cant_create_lesson_without_title(self):
    with self.assertRaises(ValidationError):
      lesson = Lesson(
        description='description',
        course=self.lesson.course,
        cover=self.lesson.cover,
        video=self.lesson.video,
        text=self.lesson.text
      )
      lesson.full_clean()
      lesson.save()
    self.assertEqual(Lesson.objects.count(), 1)

  
  def test_can_create_lesson_without_description(self):
    lesson = Lesson(
      title='lesson',
      course=self.lesson.course,
      cover=self.lesson.cover,
      video=self.lesson.video,
      text=self.lesson.text
    )
    lesson.full_clean()
    lesson.save()

    self.assertEqual(lesson.title, 'lesson')
    self.assertEqual(lesson.description, None)
    self.assertEqual(lesson.course, self.lesson.course)
    self.assertEqual(lesson.cover, self.lesson.cover)
    self.assertEqual(lesson.video, self.lesson.video)
    self.assertEqual(lesson.text, self.lesson.text)
    self.assertEqual(Lesson.objects.count(), 2)

  
  def test_cant_create_lesson_without_course(self):
    with self.assertRaises(ValidationError):
      lesson = Lesson(
        title='lesson',
        description='description',
        cover=self.lesson.cover,
        video=self.lesson.video,
        text=self.lesson.text
      )
      lesson.full_clean()
      lesson.save()
    self.assertEqual(Lesson.objects.count(), 1)

  
  def test_can_create_lesson_without_cover(self):
    lesson = Lesson(
      title='lesson',
      description='description',
      course=self.lesson.course,
      video=self.lesson.video,
      text=self.lesson.text
    )
    lesson.full_clean()
    lesson.save()

    self.assertEqual(lesson.title, 'lesson')
    self.assertEqual(lesson.description, 'description')
    self.assertEqual(lesson.course, self.lesson.course)
    self.assertEqual(lesson.cover, None)
    self.assertEqual(lesson.video, self.lesson.video)
    self.assertEqual(lesson.text, self.lesson.text)
    self.assertEqual(Lesson.objects.count(), 2)

  
  def test_can_create_lesson_without_video(self):
    lesson = Lesson(
      title='lesson',
      description='description',
      course=self.lesson.course,
      cover=self.lesson.cover,
      text=self.lesson.text
    )
    lesson.full_clean()
    lesson.save()

    self.assertEqual(lesson.title, 'lesson')
    self.assertEqual(lesson.description, 'description')
    self.assertEqual(lesson.course, self.lesson.course)
    self.assertEqual(lesson.cover, self.lesson.cover)
    self.assertEqual(lesson.video, None)
    self.assertEqual(lesson.text, self.lesson.text)
    self.assertEqual(Lesson.objects.count(), 2)

  
  def test_can_create_lesson_without_text(self):
    lesson = Lesson(
      title='lesson',
      description='description',
      course=self.lesson.course,
      cover=self.lesson.cover,
      video=self.lesson.video
    )
    lesson.full_clean()
    lesson.save()

    self.assertEqual(lesson.title, 'lesson')
    self.assertEqual(lesson.description, 'description')
    self.assertEqual(lesson.course, self.lesson.course)
    self.assertEqual(lesson.cover, self.lesson.cover)
    self.assertEqual(lesson.video, self.lesson.video)
    self.assertEqual(lesson.text, None)
    self.assertEqual(Lesson.objects.count(), 2)


  def test_cant_create_duplicate_lesson(self):
    with self.assertRaises(ValidationError):
      lesson = Lesson(
        title=self.lesson.title,
        description='description',
        course=self.lesson.course,
        cover=self.lesson.cover,
        video=self.lesson.video,
        text=self.lesson.text
      )
      lesson.full_clean()
      lesson.save()
    self.assertEqual(Lesson.objects.count(), 1)


  def test_cant_create_lesson_with_no_video_or_text(self):
    with self.assertRaises(ValidationError):
      lesson = Lesson(
        title='lesson',
        description='description',
        course=self.lesson.course,
        cover=self.lesson.cover
      )
      lesson.full_clean()
      lesson.save()
    self.assertEqual(Lesson.objects.count(), 1)

  
  def test_can_delete_lesson_with_comments(self):
    CommentFactory(lesson=self.lesson)
    self.assertEqual(self.lesson.comment_set.count(), 1)

    self.lesson.delete()

    self.assertEqual(Lesson.objects.count(), 0)
  

  def test_can_delete_lesson_with_saves(self):
    SaveFactory(lesson=self.lesson)
    self.assertEqual(self.lesson.save_set.count(), 1)

    self.lesson.delete()

    self.assertEqual(Lesson.objects.count(), 0)

  
  def test_can_delete_lesson_with_watched(self):
    WatchedFactory(lesson=self.lesson)
    self.assertEqual(self.lesson.watched_set.count(), 1)

    self.lesson.delete()

    self.assertEqual(Lesson.objects.count(), 0)