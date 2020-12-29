from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import CharField, IntegerField

class Review(models.Model):
    enrollable_id = models.IntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    rating = IntegerField()
    problems = CharField(max_length=300, default="")
    improvements = CharField(max_length=300, default="")

    def __str__(self):
        return "(enrollable={}, user={})".format(self.enrollable_id, self.user.id)
    
    class Meta:
        # Como se muestra en la web de admin
        verbose_name = "Review"
        verbose_name_plural = "Reviews"