from .plugshop.urls import get_url
from django.conf.urls import url

from apps.shop.views import *

root = get_url('plugshop')
cart_url = get_url('plugshop-cart')
product_url = get_url('plugshop-product')
product_list_url = get_url('plugshop-product-list')
category_url = get_url('plugshop-category')
order_url = get_url('plugshop-order')
order_create_url = get_url('plugshop-order-new')
category_list_url = get_url('plugshop-caterory-list')

urlpatterns = [
    url(root, ProductListView.as_view(), name='plugshop'),
    url(product_list_url, ProductListView.as_view(),
        name='plugshop-product-list'),

    url(category_list_url, CategoryListView.as_view(),
        name='plugshop-caterory-list'),
    url(category_url, CategoryView.as_view(), name='plugshop-category'),

    url(product_url, ProductView.as_view(), name='plugshop-product'),

    url(cart_url, CartView.as_view(), name="plugshop-cart"),
    url(order_url, OrderView.as_view(), name='plugshop-order'),
    url(order_create_url, OrderCreateView.as_view(), name='plugshop-order-new'),
]
