from django.db import models
from django.contrib.auth import get_user_model

ROLES =  (
    ('Estudiante','Estudiante'),
    ('Administrador', 'Administrador'),
    ('EntidadPublicoPrivada','EntidadPublicoPrivada'),
    ('Profesor','Profesor'),
)

class Request_permissions(models.Model):
    pub_date = models.DateTimeField(verbose_name="Fecha de Petición", auto_now_add=True)
    requester = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=21, choices=ROLES, default='Estudiante')
    requester_name = models.CharField(max_length=30)
    requester_email = models.EmailField(max_length=40)

    
    def __str__(self):
        return self.requester_name
    
    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Solicitud de permisos"
        verbose_name_plural = "Solicitudes de permisos"
