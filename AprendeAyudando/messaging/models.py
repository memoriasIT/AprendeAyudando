from django.db import models
from django.contrib.auth import get_user_model


class MessagingMessage(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=2000, blank=True, null=True)
    message_sent_date = models.DateTimeField(verbose_name="message sent date", auto_now_add=True)
    user_origin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='messaging_message_user_origin')
    user_destination = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='messaging_message_user_destination')