from django.db import models
from django.db.models.expressions import F
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

class UserProfile(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, default="User")
    delivery_address = models.CharField(max_length=1000, default="Default address")

    def __str__(self):

        return "{0}'s user profile".format(self.user.username)

class Review(models.Model):

    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Category(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Rating(models.Model):

    name = models.IntegerField()

    def __str__(self):
        return str(self.name)


class Product(models.Model):

    title = models.CharField(max_length=100, blank=False, default='')
    price = models.FloatField(blank=False)
    available_units = models.IntegerField(blank=False, default='')
    description = models.TextField(max_length=500, blank=False, default='')
    seller = models.TextField(max_length=100, blank=False)
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, default=True, null=False)
    ratings = models.ForeignKey(Rating, on_delete=models.CASCADE, blank=True, null=False)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_abs_url(self):
        return reverse("base:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("base:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_all_from_cart_url(self):
        return reverse("base:remove-all-from-cart", kwargs={
            'slug': self.slug
        })
    
    def get_remove_one_from_cart_url(self):
        return reverse("base:remove-one-from-cart", kwargs={
            'slug': self.slug
        })
    
    def get_add_to_wishlist_url(self):
        return reverse("base:add-to-wishlist", kwargs={
            'slug': self.slug
        })

    def get_remove_all_from_cart_add_to_wishlist_url(self):
        return reverse("base:remove-all-from-cart-add-to-wishlist", kwargs={
            'slug': self.slug
        })
        

class CartProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "{0} units of {1}".format(self.quantity, self.product.title)

class Cart(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):

        return "{0}'s cart".format(self.user.username)

class Wishlist(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct)
    added_to_cart = models.BooleanField(default=False)

    def __str__(self):

        return "{0}'s wishlist".format(self.user.username)