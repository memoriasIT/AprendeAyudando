from django.db import models
from django.contrib.auth import get_user_model

class Request_permissions(models.Model):
    pub_date = models.DateTimeField(verbose_name="date published", auto_now_add=True)
    requester = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    requester_name = models.CharField(max_length=30)
    requester_email = models.EmailField(max_length=40)

    def __str__(self):
        return self.requester_name
    
    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Solicitud de permisos"
        verbose_name_plural = "Solicitudes de permisos"
