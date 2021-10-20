from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('view-products', views.product_page, name="view-products")
]