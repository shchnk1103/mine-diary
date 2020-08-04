from blog.views import archives, categories, detail, index, tags
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('blogs/<int:pk>/', detail, name='detail'),
    path('archives/<int:year>/<int:month>/', archives, name='archives'),
    path('categories/<int:pk>/', categories, name='categories'),
    path('tags/<int:pk>/', tags, name='tags')
]
