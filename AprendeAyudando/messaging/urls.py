from django.urls import path
from . import views

app_name = 'messaging'
urlpatterns = [
    path('', views.viewMessages, name='viewMessages'),
    path('domenssage/', views.doMessage, name='doMessage'),
]