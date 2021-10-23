# """
# sources:
# https://www.bezkoder.com/django-mongodb-crud-rest-framework/
# """

# from rest_framework import serializers
# from base.models import Product

# class ProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product
#         fields = ('id', 'name', 'price', 
#         'description', 'available_units', 'seller')