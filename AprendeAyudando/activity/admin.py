from django.contrib import admin
from .models import Activity

class AdminActivity(admin.ModelAdmin):
    list_display=("title","entity","pub_date")
    search_fields=("title",)   #Para realizar barra de busqueda
    date_hierarchy="pub_date"

admin.site.register(Activity,AdminActivity)
