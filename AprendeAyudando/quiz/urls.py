from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('create/course/<int:course_id>/', views.createQuizCourse, name='createQuizCourse'),
    path('create/course/<int:course_id>/<int:quiz_course_id>/<int:number_questions>/', views.createQuestionsCourse, name='createQuestionsCourse'),
    #path('delete/<int:forum_id>/', views.delete, name='delete'), # /forum/delete/1/

]