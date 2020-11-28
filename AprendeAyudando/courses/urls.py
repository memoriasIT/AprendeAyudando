from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'), # /courses/
    path('inscription/<int:course_id>/', views.inscription, name='inscription'), # /courses/inscription/1/
    path('<int:course_id>/', views.join, name='join'), # /courses/curso/1
    path('leave/<int:course_id>/', views.leave, name='leave'), # /courses/leave/1/
    path('create/', views.createCourse, name='create'),
    path('enrolled/', views.enrolled, name='enrolled'),
]

