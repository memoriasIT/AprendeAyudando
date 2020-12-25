from django.contrib import admin
from .models import QuizCourse, QuestionCourse, AnswerCourse
# Register your models here.
class AdminQuizCourse(admin.ModelAdmin):
    list_display=("title","course","id")
    search_fields=("title",)   #Para realizar barra de busqueda
    #date_hierarchy="pub_date"

class AdminQuestionCourse(admin.ModelAdmin):
    list_display=("text","question_score","quiz","id")
    search_fields=("text","quiz",)

class AdminAnswerCourse(admin.ModelAdmin):
    list_display=("text","correct","question","id")
    search_fields=("text","question",)

admin.site.register(QuizCourse,AdminQuizCourse)
admin.site.register(QuestionCourse,AdminQuestionCourse)
admin.site.register(AnswerCourse,AdminAnswerCourse)
