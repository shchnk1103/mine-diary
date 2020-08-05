from comments.views import comment
from django.urls import path


app_name = 'comments'


urlpatterns = [
    path('comment/<int:post_pk>/', comment, name='comment'),
]
