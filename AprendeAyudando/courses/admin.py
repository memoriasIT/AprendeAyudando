from django.contrib import admin
from .models import Course, Resource

class AdminCourses(admin.ModelAdmin):
    list_display=("title","teacher","pub_date")
    search_fields=("title",)   #Para realizar barra de busqueda
    date_hierarchy="pub_date"

class AdminResources(admin.ModelAdmin):
    list_display=("resourceText", "resourceLink")
    search_fields=("resourceText",)   #Para realizar barra de busqueda
    date_hierarchy="pub_date"

admin.site.register(Course,AdminCourses)
admin.site.register(Resource,AdminResources)