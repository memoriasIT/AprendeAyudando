# Generated by Django 3.1.2 on 2020-12-31 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagingmessage',
            name='text',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]