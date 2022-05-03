from django.urls import path
from . import views


app_name = 'item'
urlpatterns = [
    path('', views.catalog, name="catalog"),
    path('<int:id>', views.get_item, name="get_item"),
    path('create', views.create_item, name="create_item"),
    path('category/<int:category_id>', views.get_category, name='get_category'),
    path('submit_offer/<int:id>', views.submit_offer, name='submit_offer'),
]
