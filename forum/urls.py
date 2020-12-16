from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('create/<int:activityCourseFk>', views.createForum, name='create'),
    path('<int:forum_id>/', views.join, name='join'), # /forum/1
    path('delete/<int:forum_id>/', views.delete, name='delete'), # /forum/delete/1/

]
