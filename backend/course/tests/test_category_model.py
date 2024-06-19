from django.test import TestCase
from course.models import Category
from course.factories import CategoryFactory
from django.core.exceptions import ValidationError
from time import sleep


class CategoryModelTestCase(TestCase):
  def setUp(self):
    self.category = CategoryFactory()

  def test_category_str(self):
    self.assertEqual(str(self.category), self.category.name)

  
  def test_can_create_valid_category(self):
    category = Category(
      name="Test Category",
      description="Test Description",
      color="#FFFFFF")
    category.full_clean()
    category.save()

    self.assertEqual(category.name, "Test Category")
    self.assertEqual(category.description, "Test Description")
    self.assertEqual(category.color, "#FFFFFF")
    self.assertTrue(category.created_at)
    self.assertTrue(category.updated_at)
    self.assertEqual(Category.objects.count(), 2)

  
  def test_cant_create_category_without_name(self):
    with self.assertRaises(ValidationError):
      category = Category(description="Test Description", color="#FFFFFF")
      category.full_clean()
      category.save()
    self.assertEqual(Category.objects.count(), 1)

  
  def test_can_create_category_without_color(self):
    category = Category(name="Test Category", description="Test Description")
    category.full_clean()
    category.save()
    self.assertEqual(category.color, "#000000")


  def test_can_update_category(self):
    category = Category(
      name="Test Category",
      description="Test Description",
      color="#FFFFFF")
    category.full_clean()
    category.save()
    
    updated_at = category.updated_at

    category.name = "Updated Category"
    category.description = "Updated Description"
    category.color = "#000000"  

    sleep(.02)
    category.full_clean()
    category.save()

    self.assertEqual(category.name, "Updated Category")
    self.assertEqual(category.description, "Updated Description")
    self.assertEqual(category.color, "#000000")
    self.assertTrue(category.created_at)
    self.assertNotEqual(category.created_at, category.updated_at)
    self.assertNotEqual(category.updated_at, updated_at)
    self.assertEqual(Category.objects.count(), 2)
    self.assertNotEqual(updated_at, category.updated_at)
    self.assertTrue(category.updated_at > updated_at)

  
  def test_delete_category(self):
    category = Category.objects.create(
      name="Test Category",
      description="Test Description",
      color="#FFFFFF")
    category.full_clean()
    category.save()
    
    self.assertEqual(Category.objects.count(), 2)

    category.delete()

    self.assertEqual(Category.objects.count(), 1)
    self.assertFalse(Category.objects.filter(name="Test Category").exists())

   