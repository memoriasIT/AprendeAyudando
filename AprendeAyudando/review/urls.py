from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'review'
urlpatterns = [
    path('create/<int:id_enrollable>/<str:title_enrollable>/', views.create, name='create'),
    path('list/<int:id_enrollable>/<str:title_enrollable>/<str:activityOrCourse>', views.list, name='list'),
    path('details/<int:id_review>/<str:title_enrollable>/', views.details, name='details'),
]