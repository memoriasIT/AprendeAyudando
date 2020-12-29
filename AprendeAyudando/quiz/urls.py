from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('create/<str:courseOrActivity>/<int:courseOrActivity_id>/', views.createQuiz, name='createQuiz'),
    path('create/<str:courseOrActivity>/<int:courseOrActivity_id>/<int:quiz_id>/<int:number_questions>/', views.createQuestions, name='createQuestions'),
    path('create/<str:courseOrActivity>/<int:courseOrActivity_id>/<int:question_id>/<int:number_questions>/<int:number_answers>/', views.createAnswers, name='createAnswers'),
    path('startquiz/<int:quiz_id>/',views.startQuiz, name='startQuiz'),
    path('doquiz/<int:quiz_id>/', views.doQuiz, name='doQuiz'),
    path('doquiz/questionasked/<int:question_id>/', views.doQuizQuestionAsked, name='doQuizQuestionAsked'),
]