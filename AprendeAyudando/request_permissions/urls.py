from django.urls import path
from . import views

app_name = 'request_permissions'
urlpatterns = [
    path('', views.index, name='index'), #/requestpermissions
]