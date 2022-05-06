from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'user'
urlpatterns = [
    path('login', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='frontpage'), name='logout'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('profile/change_password', views.change_password, name='change_password'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('contact', views.get_all_contacts, name='get_all_contacts'),
    path('contact/create', views.create_contact, name='create_contact'),
    path('contact/<int:contact_id>/update', views.update_contact, name='update_contact'),
]