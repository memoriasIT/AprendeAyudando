# Models
from .models import News
from django.db import models

# Routing
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

#Views
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView

class NewsList(ListView):
    model = News
    context_object_name = 'news_list'
    
class NewsCreate(CreateView):
    model = News
    fields = ['headline', 'content']

class NewsUpdate(UpdateView):
    model = News
    fields = ['headline', 'content']
    
class NewsDelete(DeleteView):
    model = News
    success_url = reverse_lazy('books:news-list')

class NewsDetail(DetailView):
    model = News
    context_object_name = 'news'