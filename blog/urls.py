from blog.views import ArchivesView, CategoryView, IncreaseLikeView, IndexPostListAPIView, IndexView, PostDetailView, PostViewSet, create_post, safe_delete_post, search, update_post
from django.urls import path


index = PostViewSet.as_view({'get': 'list'})

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blogs/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/',
         ArchivesView.as_view(), name='archives'),
    path('categories/<int:pk>/', CategoryView.as_view(), name='categories'),
    path('search/', search, name='search'),
    path('increase-likes/<int:id>/',
         IncreaseLikeView.as_view(), name='increase_likes'),
    path('create-post/', create_post, name='create_post'),
    path('delete-post/<int:id>/', safe_delete_post, name='post_safe_delete'),
    path('update/<int:id>/', update_post, name='update'),
    #     path('api/index/', IndexPostListAPIView.as_view()),
    path('api/index/', index),
]
