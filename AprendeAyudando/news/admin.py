from django.contrib import admin
from .models import News

class AdminNews(admin.ModelAdmin):
    list_display=("headline","creator", "pub_date")
    search_fields=("headline","creator",)   #Para realizar barra de busqueda

admin.site.register(News,AdminNews)