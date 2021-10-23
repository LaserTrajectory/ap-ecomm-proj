"""
sources:

https://www.youtube.com/watch?v=qDwdMDQ8oX4&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=3

https://www.bezkoder.com/django-mongodb-crud-rest-framework/

"""

from django.urls import path
from . import views
# from views import ProductList

urlpatterns = [
    path('', views.home, name="home"),
    path('view-products', views.product_page, name="view-products"),
    # path('product-list', views.get, name="product-list-name"),
    # url(r'^api/products$', views.product_list),
    # url(r'^api/products/(?P<pk>[0-9]+)$', views.product_detail),
    # url(r'^api/products/published$')
]