from django.db import models
from django.db.models.expressions import F

# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=100, blank=False, default='')
    price = models.FloatField(blank=False)
    available_units = models.IntegerField(blank=False, default='')
    description = models.TextField(max_length=500, blank=False, default='')
    seller = models.TextField(max_length=100, blank=False)
    kind = models.TextField(max_length=100, blank=False)