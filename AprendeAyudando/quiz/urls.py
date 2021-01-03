from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('create/<str:courseOrActivity>/<int:courseOrActivity_id>/', views.createQuiz, name='createQuiz'),
    path('create/questions/<int:quiz_id>/<int:number_questions>/', views.createQuestions, name='createQuestions'),
    path('create/answers/<int:question_id>/<int:number_questions>/<int:number_answers>/', views.createAnswers, name='createAnswers'),
    path('startquiz/<int:quiz_id>/',views.startQuiz, name='startQuiz'),
    path('doquiz/<int:quiz_id>/', views.doQuiz, name='doQuiz'),
    path('doquiz/questionasked/<int:question_id>/', views.doQuizQuestionAsked, name='doQuizQuestionAsked'),
    path('deletequiz/<int:quiz_id>/', views.deleteQuiz, name='deleteQuiz'),
    path('administrationquiz/<int:quiz_id>/', views.administrationQuiz, name='administrationQuiz'),
    path('deletequestion/<int:question_id>/', views.deleteQuestion, name='deleteQuestion'),
    path('updatequestion/<int:question_id>/', views.updateQuestion, name='updateQuestion'),
    path('updateanswers/<int:question_id>/<int:number_answers>/', views.updateAnswers, name='updateAnswers'),
    path('updatequiz/<int:quiz_id>/', views.updateQuiz, name='updateQuiz'),
    path('viewqualifications/<int:quiz_id>/', views.viewQualifications, name='viewQualifications'),
]