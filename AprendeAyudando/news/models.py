from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class News(models.Model):
    headline = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name="date published", auto_now_add=True)
    creator = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ["-pub_date"]

    def get_absolute_url(self):
        return reverse('news:news-detail', kwargs = {'pk': self.pk})