from django.urls import path
from item import views


app_name = 'item'
urlpatterns = [
    path('catalog', views.CatalogView.as_view(), name="catalog"),
    path('search', views.SearchView.as_view(), name='search'),
    path('item/<int:item_id>', views.get_item, name="get_item"),
    path('item/<int:item_id>/delete', views.delete_item, name='delete_item'),
    path('item/<int:item_id>/upload_image', views.upload_item_image, name='upload_item_image_w_item'),
    path('item/upload_image', views.upload_item_image, name='upload_item_image'),
    path('item/create', views.create_item, name="create_item"),
    path('item/offer', views.submit_offer, name='submit_offer'),

    path('offers', views.get_all_offers, name='get_all_offers'),
    path('offer/<int:offer_id>/accept', views.accept_offer, name='accept_offer'),
    path('offer/<int:offer_id>/reject', views.reject_offer, name='reject_offer'),
    path('sales', views.get_all_sales, name='get_all_sales'),
    path('sale/<int:sale_id>', views.get_sale, name='get_sale'),
    path('checkout/<int:offer_id>', views.checkout, name='checkout'),
    path('checkout/contact', views.checkout_contact, name='checkout_contact'),
    path('checkout/payment', views.checkout_payment, name='checkout_payment'),
    path('checkout/rate', views.checkout_rate, name='checkout_rate'),
    path('checkout/verify', views.checkout_verify, name='checkout_verify'),
]
