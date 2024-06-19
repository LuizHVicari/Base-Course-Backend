from django.test import TestCase
from django.core.exceptions import ValidationError
import tempfile

from course.models import Course
from course.factories import CourseFactory, LessonFactory


class TestCourseModel(TestCase):
  def setUp(self):
    self.course = CourseFactory()

  
  def test_course_str(self):
    self.assertEqual(str(self.course), self.course.title)

  
  def test_can_create_valid_course(self):
    cover_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
    course = Course(
      title="Test Course",
      description="Test Description",
      category=self.course.category,
      cover=cover_file)
    course.full_clean()
    course.save()

    self.assertEqual(course.title, "Test Course")
    self.assertEqual(course.description, "Test Description")
    self.assertEqual(course.category, self.course.category)
    self.assertEqual(course.cover, cover_file)
    self.assertTrue(course.created_at)
    self.assertTrue(course.updated_at)
    self.assertEqual(Course.objects.count(), 2)


  def test_can_create_course_without_description(self):
    cover_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
    course = Course(
      title="Test Course",
      category=self.course.category,
      cover=cover_file)
    course.full_clean()
    course.save()

    self.assertEqual(course.title, "Test Course")
    self.assertEqual(course.description, None)
    self.assertEqual(course.category, self.course.category)
    self.assertEqual(course.cover, cover_file)
    self.assertTrue(course.created_at)
    self.assertTrue(course.updated_at)
    self.assertEqual(Course.objects.count(), 2)

  
  def test_can_create_course_without_cover(self):
    course = Course(
      title="Test Course",
      description="Test Description",
      category=self.course.category)
    course.full_clean()
    course.save()

    self.assertEqual(course.title, "Test Course")
    self.assertEqual(course.description, "Test Description")
    self.assertEqual(course.category, self.course.category)
    self.assertEqual(course.cover, None)
    self.assertTrue(course.created_at)
    self.assertTrue(course.updated_at)
    self.assertEqual(Course.objects.count(), 2)

  
  def test_cant_create_course_without_title(self):
    with self.assertRaises(ValidationError):
      cover_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
      course = Course(
        description="Test Description",
        category=self.course.category,
        cover=cover_file)
      course.full_clean()
      course.save()
    self.assertEqual(Course.objects.count(), 1)


  def test_cant_create_course_without_category(self):
    with self.assertRaises(ValidationError):
      cover_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
      course = Course(
        title="Test Course",
        description="Test Description",
        cover=cover_file)
      course.full_clean()
      course.save()
    self.assertEqual(Course.objects.count(), 1)

  
  def test_can_update_course(self):
    cover_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
    course = Course(
      title="Test Course",
      description="Test Description",
      category=self.course.category,
      cover=cover_file)
    course.full_clean()
    course.save()
    
    updated_at = course.updated_at

    course.title = "Updated Course"
    course.description = "Updated Description"
    course.category = self.course.category
    course.cover = cover_file

    course.full_clean()
    course.save()

    self.assertEqual(course.title, "Updated Course")
    self.assertEqual(course.description, "Updated Description")
    self.assertEqual(course.category, self.course.category)
    self.assertEqual(course.cover, cover_file)
    self.assertTrue(course.created_at)
    self.assertNotEqual(course.created_at, course.updated_at)
    self.assertNotEqual(course.updated_at, updated_at)
    self.assertEqual(Course.objects.count(), 2)
    self.assertNotEqual(updated_at, course.updated_at)
    self.assertTrue(course.updated_at > updated_at)


  def test_can_delete_course(self):
    self.course.delete()
    self.assertEqual(Course.objects.count(), 0)

  
  def test_cant_create_course_with_same_title(self):
    with self.assertRaises(ValidationError):
      cover_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
      course = Course(
        title=self.course.title,
        description="Test Description",
        category=self.course.category,
        cover=cover_file)
      course.full_clean()
      course.save()
    self.assertEqual(Course.objects.count(), 1)

  
  def test_can_delete_course_with_lessons(self):
    course = CourseFactory()
    LessonFactory(course=course)
    self.assertEqual(Course.objects.count(), 2)
    self.assertEqual(course.lesson_set.count(), 1)
    course.delete()
    self.assertEqual(Course.objects.count(), 1)


  