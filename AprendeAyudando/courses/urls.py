from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'), # /courses/
    path('inscription/<int:course_id>/', views.inscription, name='inscription'), # /courses/inscription/1/
    path('<int:course_id>/', views.join, name='join'), # /courses/curso/1
    path('leave/<int:course_id>/', views.leave, name='leave'), # /courses/leave/1/
    path('create/', views.createCourse, name='create'),
    path('update/<int:course_id>', views.update, name='update'),
    path('enrolled/', views.enrolled, name='enrolled'),
    path('delete/<int:course_id>/', views.delete, name='delete'), # /courses/delete/1/
    path('users/<int:course_id>/', views.users, name='users'), # /courses/users/1/
    path('removeUser/<int:course_id>/<int:user_id>/', views.removeUser, name='removeUser'),
    path('banned/<int:course_id>/', views.banned, name='banned'), # /courses/users/1/ 
]

