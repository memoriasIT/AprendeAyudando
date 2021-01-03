# Generated by Django 3.1.3 on 2021-01-03 13:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20210103_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='dateInCalendar',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resource',
            name='isLocalFile',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
