from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('create/course/<int:course_id>', views.createQuizCourse, name='createQuizCourse'),
    #path('<int:forum_id>/', views.join, name='join'), # /forum/1
    #path('delete/<int:forum_id>/', views.delete, name='delete'), # /forum/delete/1/

]