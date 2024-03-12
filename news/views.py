from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef

from .models import Post, Category, Subscriber
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    ordering = '-dataPost'
    template_name = 'newslist.html'
    context_object_name = 'newslist'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['total_post'] = Post.objects.count()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post - {self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post - {self.kwargs["pk"]}', obj)
            return obj


class PostSearch(ListView):
    model = Post
    ordering = '-dataPost'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        context['filter_post'] = self.filterset.qs.count()
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.typePost = post.newsPost
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.typePost = post.articlePost
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk')
            )
        )
    ).order_by('subject')

    return render(
        request,
        'subscription.html',
        {'categories': categories_with_subscriptions},
    )

