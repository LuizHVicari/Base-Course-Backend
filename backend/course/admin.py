from django.contrib import admin
from .models import Category, Course, Lesson, Comment, Save

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'description', 'color')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'category', 'cover')

  
@admin.register(Lesson)
class ClassAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'course', 'cover', 'video', 'text')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ('user', 'text', 'stars', 'lesson', 'comment_fk', 'created_at', 'updated_at')


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
  list_display = ('user', 'lesson')