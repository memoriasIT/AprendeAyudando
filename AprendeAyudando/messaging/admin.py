from django.contrib import admin
from .models import MessagingMessage

class AdminMessagingMessage(admin.ModelAdmin):
    list_display=("title","user_origin","user_destination","message_sent_date")
    search_fields=("title","user_origin","user_destination")   #Para realizar barra de busqueda
    date_hierarchy="message_sent_date"


admin.site.register(MessagingMessage,AdminMessagingMessage)
