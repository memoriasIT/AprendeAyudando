from django.contrib import admin
from .models import Quiz, Question, Answer, Qualification, QuestionAsked #Prue
# Register your models here.
"""class AdminQuizCourse(admin.ModelAdmin):
    list_display=("title","course","id")
    search_fields=("title",)   #Para realizar barra de busqueda
    #date_hierarchy="pub_date"
class AdminQuestionCourse(admin.ModelAdmin):
    list_display=("text","question_score","quiz","id")
    search_fields=("text","quiz",)

class AdminAnswerCourse(admin.ModelAdmin):
    list_display=("text","correct","question","id")
    search_fields=("text","question",)

class AdminQualificationCourse(admin.ModelAdmin):
    list_display=("user","quiz","total_score","id")
    search_fields=("user","quiz",)

class AdminQuestionAskedCourse(admin.ModelAdmin):
    list_display=("qualification_course","question_course","id")
    search_fields=("qualification_course","question_course",)

class AdminQuizActivity(admin.ModelAdmin):
    list_display=("title","activity","id")
    search_fields=("title",)   #Para realizar barra de busqueda
    #date_hierarchy="pub_date"""


    
"""class AdminPrue(admin.ModelAdmin):
    list_display=("texto","quiz_activity","quiz_course", "id")
    search_fields=("texto","id",)"""

"""admin.site.register(QuizCourse,AdminQuizCourse)
admin.site.register(QuestionCourse,AdminQuestionCourse)
admin.site.register(AnswerCourse,AdminAnswerCourse)
admin.site.register(QualificationCourse,AdminQualificationCourse)
admin.site.register(QuestionAskedCourse,AdminQuestionAskedCourse)
admin.site.register(QuizActivity,AdminQuizActivity)"""

#admin.site.register(Prue,AdminPrue)
class AdminQuiz(admin.ModelAdmin):
    list_display=("title","course","activity","id")
    search_fields=("title",)   #Para realizar barra de busqueda
    #date_hierarchy="pub_date"
class AdminQuestion(admin.ModelAdmin):
    list_display=("text","question_score","quiz","id")
    search_fields=("text","quiz",)

class AdminAnswer(admin.ModelAdmin):
    list_display=("text","correct","question","id")
    search_fields=("text","question",)

class AdminQualification(admin.ModelAdmin):
    list_display=("user","quiz","total_score","id")
    search_fields=("user","quiz",)

class AdminQuestionAsked(admin.ModelAdmin):
    list_display=("qualification","question","id")
    search_fields=("qualification","question",)

admin.site.register(Quiz,AdminQuiz)
admin.site.register(Question,AdminQuestion)
admin.site.register(Answer,AdminAnswer)
admin.site.register(Qualification,AdminQualification)
admin.site.register(QuestionAsked,AdminQuestionAsked)