# Generated by Django 3.1.2 on 2020-11-30 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20201130_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='enrolled_users',
        ),
    ]