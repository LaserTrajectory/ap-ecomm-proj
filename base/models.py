from django.db import models

# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=100, blank=False, default='')
    price = models.FloatField(blank=False)
    available_units = models.IntegerField(blank=False)
    description = models.TextField(max_length=500, blank=False, default='')
    seller = models.TextField(max_length=100, blank=False)