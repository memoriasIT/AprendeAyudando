from django.contrib import admin
from .models import Quiz, Question, Answer, Qualification, QuestionAsked
class AdminQuiz(admin.ModelAdmin):
    list_display=("title","course","activity","id")
    search_fields=("title",)

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