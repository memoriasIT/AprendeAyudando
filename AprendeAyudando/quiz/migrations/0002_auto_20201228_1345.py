# Generated by Django 3.1.2 on 2020-12-28 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='qualification',
            name='total_correct_questions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quiz',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='Maximum Date'),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]