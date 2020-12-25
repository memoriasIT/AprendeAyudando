from django.contrib import admin
from .models import QuizCourse, QuestionCourse
# Register your models here.
class AdminQuizCourse(admin.ModelAdmin):
    list_display=("title","course","id")
    search_fields=("title",)   #Para realizar barra de busqueda
    #date_hierarchy="pub_date"

class AdminQuestionCourse(admin.ModelAdmin):
    list_display=("text","question_score","quiz","id")
    search_fields=("text","quiz",) 
admin.site.register(QuizCourse,AdminQuizCourse)
admin.site.register(QuestionCourse,AdminQuestionCourse)
