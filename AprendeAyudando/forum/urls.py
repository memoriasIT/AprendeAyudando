from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('create/<str:courseOrActivity>/<int:activityCourseFk>', views.createForum, name='create'),
    path('<int:forum_id>/', views.join, name='join'), # /forum/1
    path('delete/<int:forum_id>/', views.delete, name='delete'), # /forum/delete/1/
    path('updateForum/<int:forum_id>/', views.updateForum, name='updateForum'), # /forum/updateForum/1/
    #DEBATES
    path('debate/<int:debate_id>', views.viewDebate, name='viewDebate'),
    path('createDebate/<int:forum_id>', views.createDebate, name='createDebate'),
    path('deleteDebate/<int:debate_id>', views.deleteDebate, name='deleteDebate'),
    #MESAJES
    path('reply/<int:message_id>', views.reply, name='reply'),
    path('deleteMessage/<int:message_id>', views.deleteMessage, name='deleteMessage'),
    

    
]
