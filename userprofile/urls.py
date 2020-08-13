from userprofile.views import profile_edit, user_login, user_logout, user_register
from django.urls import path, include


app_name = 'userprofile'

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', user_register, name='user_register'),
    path('edit/<int:id>/', profile_edit, name='profile_edit'),
]
