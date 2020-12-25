from django.contrib import admin
from .models import QuizCourse
# Register your models here.
class AdminQuizCourse(admin.ModelAdmin):
    list_display=("title","course","id")
    search_fields=("title",)   #Para realizar barra de busqueda
    #date_hierarchy="pub_date"

admin.site.register(QuizCourse,AdminQuizCourse)
