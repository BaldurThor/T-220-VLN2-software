from django.urls import path
from . import views


app_name = 'item'
urlpatterns = [
    path('', views.CatalogView.as_view(), name="catalog"),
    path('search', views.SearchView.as_view(), name='search'),
    path('<int:id>', views.get_item, name="get_item"),
    path('<int:item_id>/delete', views.delete_item, name='delete_item'),
    path('create', views.create_item, name="create_item"),
    path('submit_offer/<int:id>', views.submit_offer, name='submit_offer'),
    path('get_all_offers', views.get_all_offers, name='get_all_offers'),
    path('accept_offer/<int:offer_id>', views.accept_offer, name='accept_offer'),
    path('reject_offer/<int:offer_id>', views.reject_offer, name='reject_offer'),
    path('get_all_sales', views.get_all_sales, name='get_all_sales'),
    path('get_sale/<int:sale_id>', views.get_sale, name='get_sale'),
    path('checkout/<int:offer_id>', views.checkout, name='checkout'),
    path('checkout/contact', views.checkout_contact, name='checkout_contact'),
    path('checkout/payment', views.checkout_payment, name='checkout_payment'),
    path('checkout/rate', views.checkout_rate, name='checkout_rate'),
    path('checkout/verify', views.checkout_verify, name='checkout_verify'),
    path('checkout/thanks', views.checkout_thanks, name='checkout_thanks'),
]
