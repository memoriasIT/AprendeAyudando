from django.urls import path
from . import views

app_name = 'activity'
urlpatterns = [
    path('', views.index, name='index'), # /activity/
    path('inscription/<int:activity_id>/', views.inscription, name='inscription'), # /activity/inscripcion/1/
    path('<int:activity_id>/', views.join, name='join'), # /activity/curso/1
    path('leave/<int:activity_id>/', views.leave, name='leave'), # /activity/leave/1/
    path('create/', views.createActivity, name='create'),
    path('delete/<int:activity_id>/', views.delete, name='delete'), # /activity/delete/1/,
    path('enrolled/', views.enrolled, name='enrolled'),
    path('<int:activity_id>/activityrequest/', views.view_activity_request, name='activityrequest'),
    path('<int:activity_id>/action_activity_request/', views.action_activity_request, name='action_activity_request'),
    path('users/<int:activity_id>/', views.users, name='users'), # /activity/users/1/
    path('removeUser/<int:activity_id>/<int:user_id>/', views.removeUser, name='removeUser'), 
    path('banned/<int:activity_id>/', views.banned, name='banned'), # /activity/banned/1/ 
]
