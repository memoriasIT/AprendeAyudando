from django.contrib import admin
from .models import Course #, Activity

class AdminCourses(admin.ModelAdmin):
    list_display=("title","teacher","pub_date")
    search_fields=("title",)   #Para realizar barra de busqueda
    date_hierarchy="pub_date"

admin.site.register(Course,AdminCourses)