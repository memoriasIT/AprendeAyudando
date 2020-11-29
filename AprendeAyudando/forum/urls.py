from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('create/', views.createForum, name='create'),
    path('delete/<int:forum_id>/', views.delete, name='delete'), # /forum/delete/1/
    path('<int:forum_id>/', views.details, name='join'), # /forum/1
]
