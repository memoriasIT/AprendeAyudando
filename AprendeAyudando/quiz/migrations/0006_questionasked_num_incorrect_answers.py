# Generated by Django 3.1.2 on 2020-12-29 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20201229_0440'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionasked',
            name='num_incorrect_answers',
            field=models.IntegerField(default=0),
        ),
    ]