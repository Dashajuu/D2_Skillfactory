from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-dataPost'
    template_name = 'newslist.html'
    context_object_name = 'newslist'


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'