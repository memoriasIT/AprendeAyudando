from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('create/', views.createForum, name='create'),
    # path('delete/', views.deleteForum, name='delete'),
]
