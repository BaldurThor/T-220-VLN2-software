from django.contrib import admin
from django.urls import path
from . import views
app_name = 'messaging'
urlpatterns = [
    path('', views.get_all_messages, name='get_all_messages'),
    path('<int:message_id>', views.get_message, name='get_message'),
    path('send', views.send_message, name='send'),
]
