# Generated by Django 3.1.2 on 2020-12-05 02:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activity', '0002_activity_restricted_entry'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.activity')),
                ('requester', models.ForeignKey(limit_choices_to=models.Q(groups__name='Estudiante'), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Solicitud de Actividad',
                'verbose_name_plural': 'Solicitudes de Actividades',
            },
        ),
    ]
