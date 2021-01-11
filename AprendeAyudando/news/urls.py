from django.urls import path
from . import views
from news.views import (NewsList, NewsCreate, NewsDetail, NewsUpdate, NewsDelete)


app_name = 'news'
urlpatterns = [
    path('', NewsList.as_view(), name='news-list'),
    path('news/add/', NewsCreate.as_view(), name='news-add'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news-update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news-delete'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),
]