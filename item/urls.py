from django.urls import path
from . import views


app_name = 'item'
urlpatterns = [
    path('', views.catalog, name="catalog"),
    path('<int:id>', views.get_item, name="get_item"),
    path('create', views.create_item, name="create_item"),
    path('category/<int:category_id>', views.get_category, name='get_category'),
    path('submit_offer/<int:id>', views.submit_offer, name='submit_offer'),
    path('get_all_offers', views.get_all_offers, name='get_all_offers'),
    path('accept_offer/<int:offer_id>', views.accept_offer, name='accept_offer'),
    path('reject_offer/<int:offer_id>', views.reject_offer, name='reject_offer'),
    path('checkout/<int:offer_id>', views.checkout, name='checkout'),
    path('get_all_sales', views.get_all_sales, name='get_all_sales'),
    path('get_sale/<int:sale_id>', views.get_sale, name='get_sale'),
]
