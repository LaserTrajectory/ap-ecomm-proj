from django.contrib import admin
from .models import CartProduct, Product, Category, Rating, Cart, CartProduct, Wishlist, UserProfile, ReviewProduct
# Register your models here.

admin.site.register(Product)
admin.site.register(ReviewProduct)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Wishlist)
admin.site.register(UserProfile)