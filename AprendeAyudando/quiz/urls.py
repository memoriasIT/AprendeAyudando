from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('create/quizcourse/<int:course_id>/', views.createQuizCourse, name='createQuizCourse'),
    path('create/quizcourse/<int:course_id>/<int:quiz_course_id>/<int:number_questions>/', views.createQuestionsCourse, name='createQuestionsCourse'),
    path('create/quizcourse/<int:course_id>/<int:question_course_id>/<int:number_questions>/<int:number_answers>/', views.createAnswersCourse, name='createAnswersCourse'), # /forum/delete/1/

]