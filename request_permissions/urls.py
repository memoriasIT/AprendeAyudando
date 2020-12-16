from django.urls import path
from . import views

app_name = 'request_permissions'
urlpatterns = [
    path('', views.index, name='index'), #/requestpermissions
    path('create/<str:requestType>', views.createRequest, name='create'),
    path('give/', views.give_permissions, name='give_permissions'),
    path('accept/<int:request_id>/', views.accept, name='accept'),
    path('deny/<int:request_id>/', views.deny, name='deny'),
    path('redirectForm/<str:requestType>', views.redirectForm, name='redirectForm'),
]
