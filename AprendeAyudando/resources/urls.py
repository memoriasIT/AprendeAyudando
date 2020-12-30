from django.urls import path
from . import views

app_name = 'resources'
urlpatterns = [
    path('create/<str:courseOrActivity>/<int:activityCourseFk>', views.createResource, name='createResource'), # /resource/create/1/
    path('delete/<int:resource_id>/', views.delete, name='delete'), # /resource/delete/1/
]
