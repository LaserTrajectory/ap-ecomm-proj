from django.db import models
from django.db.models.expressions import F
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

class Reviews(models.Model):

    name = models.CharField(max_length=50)

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
    reviews = models.ForeignKey(Reviews, on_delete=models.CASCADE)
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

    def get_remove_from_cart_url(self):
        return reverse("base:remove-from-cart", kwargs={
            'slug': self.slug
        })
        

class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            blank=True, null=True)
    is_ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} units of {self.product.title}"

class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    origin_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    products = models.ManyToManyField(OrderProduct)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):

        return self.user.username
        # return "{0}'s order".format(self.user.username)
