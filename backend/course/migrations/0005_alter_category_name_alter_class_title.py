# Generated by Django 5.0.6 on 2024-06-19 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_alter_course_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
