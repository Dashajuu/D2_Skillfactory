from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (PostList, PostDetail, PostSearch, NewsCreate, ArticleCreate, PostUpdate, PostDelete)


urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', cache_page(60)(PostSearch.as_view()), name='search_results'),
    path('search/<int:pk>', PostDetail.as_view()),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/update', PostUpdate.as_view(), name='news_update'),
    path('article/<int:pk>/update', PostUpdate.as_view(), name='article_update'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('article/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
]
