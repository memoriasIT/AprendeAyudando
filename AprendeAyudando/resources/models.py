from django.db import models

# Create your models here.
class Resource(models.Model):
    activityCourseFk = models.IntegerField()
    activityCourseType = models.CharField(max_length=20)
    resourceText = models.CharField(max_length=200)
    isLocalFile = models.BooleanField()
    resourceLink = models.CharField(max_length=200, blank=True, null=True)
    file = models.FileField(null=False, blank=False, default=None)
    isShownInCalendar = models.BooleanField()
    dateInCalendar  = models.DateField(blank=True, null=True)
    pub_date = models.DateTimeField(verbose_name="date published", auto_now_add=True)

    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"