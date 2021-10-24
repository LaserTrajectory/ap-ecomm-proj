from django.db import models
from django.db.models.expressions import F

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

    def __str__(self):
        return self.title