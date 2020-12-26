from django.db import models

from django.contrib.auth import get_user_model
from django.db.models import Q

class Activity(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name="date published", auto_now_add=True)
    enrolled_users = models.ManyToManyField(get_user_model(), related_name="activities", blank=True)
    banned_users = models.ManyToManyField(get_user_model(), related_name="bannedActivities", blank=True)
    entity = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, limit_choices_to={'groups__name':'EntidadPublicoPrivada'})
    restricted_entry = models.BooleanField(null=True) #Aun falta añadir esta funcionalidad(recordad hacer el makemigrations->migrate si lo implementais)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return self.title
    
    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"


class ActivityRequest(models.Model):
    requester = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to=Q(groups__name='Estudiante'))
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(verbose_name="date published", auto_now_add=True, null=True)
    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Solicitud de Actividad"
        verbose_name_plural = "Solicitudes de Actividades"
        unique_together = ('requester', 'activity')