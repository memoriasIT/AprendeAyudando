from django.urls import path
from . import views

app_name = 'messaging'
urlpatterns = [
    path('', views.index, name='index'),
    path('domenssage/', views.doMessage, name='doMessage'),
    path('viewmessage/<int:message_id>/', views.viewMessage, name='viewMessage'),
]