from django.contrib import admin
from .models import Category, Course, Class, Comment, Save

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'description', 'color')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'category', 'cover')

  
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'course', 'cover', 'video', 'text')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ('user', 'text', 'stars', 'class_fk', 'comment_fk', 'created_at', 'updated_at')


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
  list_display = ('user', 'class_fk')