# Generated by Django 3.1.2 on 2020-12-29 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20201228_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_negative_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionasked',
            name='num_correct_answers',
            field=models.IntegerField(default=0),
        ),
    ]