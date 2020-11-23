from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'), # /courses/
    path('<int:course_id>/', views.details, name='detail'), # /courses/1/
    path('join/<int:course_id>/', views.join, name='join'), # /courses/join/1/
    path('leave/<int:course_id>/', views.leave, name='leave'), # /courses/join/1/
]

