# Generated by Django 3.1.3 on 2020-12-01 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request_permissions', '0002_request_permissions_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request_permissions',
            name='requester_email',
        ),
        migrations.RemoveField(
            model_name='request_permissions',
            name='requester_name',
        ),
        migrations.AlterField(
            model_name='request_permissions',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Petición'),
        ),
    ]
