from django.urls import path
from . import views

app_name = 'activity'
urlpatterns = [
    path('', views.index, name='index'), # /activity/
    path('inscription/<int:activity_id>/', views.inscription, name='inscription'), # /activity/inscription/1/
    path('<int:activity_id>/', views.join, name='join'), # /activity/1/
    path('leave/<int:activity_id>/', views.leave, name='leave'), # /activity/leave/1/
    path('create/', views.createActivity, name='create'), #/activity/create/
     path('update/<int:activity_id>/', views.update, name='update'), # /activity/update/1/
    path('delete/<int:activity_id>/', views.delete, name='delete'), # /activity/delete/1/,
    path('enrolled/', views.enrolled, name='enrolled'),# /activity/enrolled/
    path('<int:activity_id>/activityrequest/', views.view_activity_request, name='activityrequest'), # /activity/1/activityrequest/
    path('<int:activity_id>/action_activity_request/', views.action_activity_request, name='action_activity_request'), # /activity/1/action_activityrequest/
    path('users/<int:activity_id>/', views.users, name='users'), # /activity/users/1/
    path('removeUser/<int:activity_id>/<int:user_id>/', views.removeUser, name='removeUser'), # /activity/removeUser/1/30/
    path('banned/<int:activity_id>/', views.banned, name='banned'), # /activity/banned/1/ 
]
