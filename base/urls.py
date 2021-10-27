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
    path('view-products', views.ProductView.as_view(), name='view-products'),
    path('search-form', views.SearchFilterView, name="search-filter"),
    path('profile', views.profile, name="profile"),
    path("logout", views.logout),
    path('', views.index, name='auth'),
    path('', include("django.contrib.auth.urls")),
    path('', include("social_django.urls", namespace='social')),
    # path('products', views.products, name='products')
    path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>', views.add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>', views.remove_from_cart, name="remove-from-cart")
    
]