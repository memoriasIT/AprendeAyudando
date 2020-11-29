from django.contrib import admin
from .models import Forum


class AdminForum(admin.ModelAdmin):
    list_display=("title","teacher")
    search_fields=("title",)   #Para realizar barra de busqueda

admin.site.register(Forum,AdminForum)