from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

class Forum(models.Model):
    title = models.CharField(max_length=200)
    #enrolled_users = models.ManyToManyField(get_user_model(), related_name="forums", blank=True)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, 
                                limit_choices_to=Q(groups__name='Profesor') | Q(groups__name='EntidadPublicoPrivada'))

    def __str__(self):
        return self.title
    
    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Foro"
        verbose_name_plural = "Foros"
