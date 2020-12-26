from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

class Forum(models.Model):
    title = models.CharField(max_length=200)
    enrolled_users = models.ManyToManyField(get_user_model(), related_name="forums", blank=True)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, 
                                limit_choices_to=Q(groups__name='Profesor') | Q(groups__name='EntidadPublicoPrivada'))
    activityCourseFk = models.IntegerField()
    activityCourseType = models.CharField(max_length=20)
    def __str__(self):
        return self.title
    
    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Foro"
        verbose_name_plural = "Foros"


class Debate(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Debate"
        verbose_name_plural = "Debates"

class Message(models.Model):
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.CharField(max_length=2000, blank=True)
    pub_date = models.DateTimeField(verbose_name="date published", auto_now_add=True)
    debate = models.ForeignKey(Debate, on_delete=models.CASCADE)
    initial = models.BooleanField(null=True)
    def __str__(self):
        return self.subject + ' by ' + self.author.email

    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"

class Reply(models.Model):
    originalMessage = models.ForeignKey(Message, related_name='originalMessage', on_delete=models.CASCADE)
    replyMessage = models.ForeignKey(Message, related_name='replyMessage', on_delete=models.CASCADE)

    def __str__(self):
        return 'OM: ' + self.originalMessage.subject + ', RM: ' + self.replyMessage.subject

    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"