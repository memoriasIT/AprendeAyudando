#Forms
from django.forms import ModelForm, Textarea

from .forms import NewsForm

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
    form_class = NewsForm
    model = News
    success_url = reverse_lazy('news:news-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isCreate'] = True
        context['user'] = self.request.user
        return context
    
class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = News
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isCreate'] = False
        return context
    
class NewsDelete(DeleteView):
    model = News
    success_url = reverse_lazy('news:news-list')

class NewsDetail(DetailView):
    model = News
    context_object_name = 'news'