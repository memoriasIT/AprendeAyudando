# Generated by Django 3.1.3 on 2020-12-09 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('description', models.CharField(max_length=1000)),
                ('enrolled_users', models.ManyToManyField(blank=True, related_name='courses', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(limit_choices_to={'groups__name': 'Profesor'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resourceText', models.CharField(max_length=200)),
                ('resourceLink', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
            options={
                'verbose_name': 'Recurso',
                'verbose_name_plural': 'Recursos',
            },
        ),
    ]
