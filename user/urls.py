from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'user'
urlpatterns = [
    path('login', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='frontpage'), name='logout'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('update_profile', views.update_profile, name='update_profile'),
]
