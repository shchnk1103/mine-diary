from blog.views import ArchivesView, CategoryView, IncreaseLikeView, IndexView, PostDetailView, TagsViews, create_post, safe_delete_post, search
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blogs/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/',
         ArchivesView.as_view(), name='archives'),
    path('categories/<int:pk>/', CategoryView.as_view(), name='categories'),
    path('tags/<int:pk>/', TagsViews.as_view(), name='tags'),
    path('search/', search, name='search'),
    path('increase-likes/<int:id>/',
         IncreaseLikeView.as_view(), name='increase_likes'),
    path('create-post/', create_post, name='create_post'),
    path('delete-post/<int:id>/', safe_delete_post, name='post_safe_delete'),
]
