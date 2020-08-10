from userprofile.views import user_login, user_logout, user_register
from django.urls import path, include


app_name = 'userprofile'

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', user_register, name='user_register'),
]
