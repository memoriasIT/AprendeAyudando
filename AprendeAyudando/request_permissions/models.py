from django.db import models
from django.contrib.auth import get_user_model

ESTUDIANTE = 'Estudiante'
ADMINISTRADOR = 'Administrador'
ENTIDADPUBLICOPRIVADA = 'EntidadPublicoPrivada'
PROFESOR = 'Profesor'

ROLES =  (
    (ESTUDIANTE, ESTUDIANTE),
    (ADMINISTRADOR, ADMINISTRADOR),
    (ENTIDADPUBLICOPRIVADA, ENTIDADPUBLICOPRIVADA),
    (PROFESOR,PROFESOR),
)

class Request_permissions(models.Model):
    pub_date = models.DateTimeField(verbose_name="Fecha de Petición", auto_now_add=True)
    requester = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=25, choices=ROLES, default='Estudiante')
    requester_name = models.CharField(max_length=30, null=True, blank=True)
    requester_email = models.EmailField(max_length=40, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    organization_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.requester_name
    
    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Solicitud de permisos"
        verbose_name_plural = "Solicitudes de permisos"
