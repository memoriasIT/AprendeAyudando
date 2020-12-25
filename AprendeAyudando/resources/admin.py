from django.contrib import admin
from .models import Resource

# Register your models here.
class AdminResources(admin.ModelAdmin):
    list_display=("resourceText", "resourceLink")
    search_fields=("resourceText",)   #Para realizar barra de busqueda
    date_hierarchy="pub_date"

admin.site.register(Resource,AdminResources)