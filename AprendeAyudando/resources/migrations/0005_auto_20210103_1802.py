# Generated by Django 3.1.3 on 2021-01-03 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_auto_20210103_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='resourceLink',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
