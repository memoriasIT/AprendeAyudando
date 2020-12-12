from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

class UserInfo(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, 
                                limit_choices_to=Q(groups__name='Profesor') | Q(groups__name='EntidadPublicoPrivada'))
    phone = models.CharField(max_length=12)
    organization_name = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username

