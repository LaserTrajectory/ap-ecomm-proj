"""
sources:

https://www.youtube.com/watch?v=qDwdMDQ8oX4&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=3

https://www.bezkoder.com/django-mongodb-crud-rest-framework/

"""

from django.urls import path, include
from . import views
# from views import ProductList

app_name = 'base'

urlpatterns = [
    path('home', views.home, name="home"),
    path('view-products', views.product_page, name='view-products'),
    path('search-form', views.SearchFilterView, name="search-filter"),
    path('autosuggestion-title', views.autosuggestion_title, name="autosuggestion-title"),
    path('profile', views.profile, name="profile"),
    path("logout", views.logout),
    path('', views.index, name='auth'),
    path('', include("django.contrib.auth.urls")),
    path('', include("social_django.urls", namespace='social')),
    # path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),
    path('product/<slug>', views.products, name='product'),
    path('add-to-cart/<slug>', views.add_to_cart, name="add-to-cart"),
    path('remove-all-from-cart/<slug>', views.remove_all_from_cart, name="remove-all-from-cart"),
    path('remove-one-from-cart/<slug>', views.remove_one_from_cart, name="remove-one-from-cart"),
    path('cart', views.cart_view, name='cart'),
    path('add-to-wishlist/<slug>', views.add_to_wishlist, name="add-to-wishlist"),
    path('wishlist', views.wishlist_view, name='wishlist'),
    path('remove-all-from-cart-add-to-wishlist/<slug>', views.remove_all_from_cart_add_to_wishlist, name="remove-all-from-cart-add-to-wishlist"),
    path('edit-profile', views.edit_profile, name="edit-profile"),
    path('checkout', views.checkout, name="checkout"),
    path('order', views.order_summary, name="order-summary"),
    path('my-orders', views.my_orders, name="my-orders")
]