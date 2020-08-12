from blog.views import ArchivesView, CategoryView, IncreaseLikeView, IndexView, PostDetailView, TagsViews, search
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
]
