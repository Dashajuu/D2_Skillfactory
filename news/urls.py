from django.urls import path
from .views import PostList, PostDetail, PostSearch, NewsCreate, ArticleCreate, PostUpdate, PostDelete


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='search_results'),
    path('search/<int:pk>', PostDetail.as_view()),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/update', PostUpdate.as_view()),
    path('article/<int:pk>/update', PostUpdate.as_view()),
    path('news/<int:pk>/delete', PostDelete.as_view()),
    path('article/<int:pk>/delete', PostDelete.as_view()),
]
