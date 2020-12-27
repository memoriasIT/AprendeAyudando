from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('create/<str:courseOrActivity>/<int:courseOrActivity_id>/', views.createQuizCourse, name='createQuizCourse'),
    path('create/<str:courseOrActivity>/<int:courseOrActivity_id>/<int:quiz_id>/<int:number_questions>/', views.createQuestionsCourse, name='createQuestionsCourse'),
    path('create/<str:courseOrActivity>/<int:courseOrActivity_id>/<int:question_id>/<int:number_questions>/<int:number_answers>/', views.createAnswersCourse, name='createAnswersCourse'),
    path('startquiz/quizcourse/<int:quiz_id>/',views.startQuiz, name='startQuiz'),
    path('doquiz/quizcourse/<int:quiz_id>/', views.doQuizCourse, name='doQuizCourse'),
    path('doquiz/quizcourse/questionasked/<int:question_id>/', views.doQuizCourseQuestionAsked, name='doQuizCourseQuestionAsked'),
]