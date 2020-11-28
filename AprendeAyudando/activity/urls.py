from django.urls import path
from . import views

app_name = 'activity'
urlpatterns = [
    path('', views.index, name='index'), # /activity/
    path('inscription/<int:activity_id>/', views.inscription, name='inscription'), # /activity/inscripcion/1/
    path('<int:activity_id>/', views.join, name='join'), # /activity/curso/1
    path('leave/<int:activity_id>/', views.leave, name='leave'), # /activity/leave/1/
    path('create/', views.createActivity, name='create'),
]