from blog.views import detail, index
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('blogs/<int:pk>/', detail, name='detail'),
]
