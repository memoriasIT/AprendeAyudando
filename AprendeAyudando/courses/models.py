from django.db import models
from django.contrib.auth import get_user_model


class Course(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name="date published", auto_now_add=True)
    enrolled_users = models.ManyToManyField(get_user_model(), related_name="courses", blank=True)
    teacher = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, limit_choices_to={'groups__name':'Profesor'})

    def __str__(self):
        return self.title
    
    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"


#  MEJOR HACERLO EN OTRA CARPETA?
# class Activity(models.Model):
#     title = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')

#     def __str__(self):
#         return self.title

#     class Meta:
#         # Como se muestra en la web de admin
#         verbose_name = "Actividad"
#         verbose_name_plural = "Actividades"
