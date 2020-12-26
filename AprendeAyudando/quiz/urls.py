from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('create/quizcourse/<int:course_id>/', views.createQuizCourse, name='createQuizCourse'),
    path('create/quizcourse/<int:course_id>/<int:quiz_course_id>/<int:number_questions>/', views.createQuestionsCourse, name='createQuestionsCourse'),
    path('create/quizcourse/<int:course_id>/<int:question_course_id>/<int:number_questions>/<int:number_answers>/', views.createAnswersCourse, name='createAnswersCourse'),
    path('startquiz/quizcourse/<int:quiz_id>/',views.startQuiz, name='startQuiz'),
    path('doquiz/quizcourse/<int:quiz_id>/', views.doQuizCourse, name='doQuizCourse'),
    path('doquiz/quizcourse/questionasked/<int:question_id>/', views.doQuizCourseQuestionAsked, name='doQuizCourseQuestionAsked'),
]