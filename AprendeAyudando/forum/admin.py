from django.contrib import admin
from .models import Forum


class AdminForum(admin.ModelAdmin): 
    pass
    list_display=("title","author")
    search_fields=("title",)   #Para realizar barra de busqueda

admin.site.register(Forum,AdminForum)