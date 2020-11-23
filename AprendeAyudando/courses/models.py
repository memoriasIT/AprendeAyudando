from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

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