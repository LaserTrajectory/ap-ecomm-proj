from django.contrib import admin
from .models import Product, Reviews, Category, Rating
# Register your models here.

admin.site.register(Product)
admin.site.register(Reviews)
admin.site.register(Category)
admin.site.register(Rating)