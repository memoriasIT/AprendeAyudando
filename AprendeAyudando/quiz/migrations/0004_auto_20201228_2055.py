# Generated by Django 3.1.2 on 2020-12-28 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20201228_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='maximum_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Maximum Date'),
        ),
    ]
