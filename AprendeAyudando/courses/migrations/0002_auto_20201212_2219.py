# Generated by Django 3.1.2 on 2020-12-12 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
