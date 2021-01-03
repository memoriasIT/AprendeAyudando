# Generated by Django 3.1.3 on 2021-01-03 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='file',
            field=models.FileField(default='a', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resource',
            name='isShownInCalendar',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
