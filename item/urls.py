from django.urls import path
from . import views


app_name = 'item'
urlpatterns = [
    path('', views.catalog, name="catalog"),
    path('<int:id>', views.get_item, name="get_item"),
    path('create', views.create_item, name="create_item")
]
