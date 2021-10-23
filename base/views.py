from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# from rest_framework.renderers import TemplateHTMLRenderer
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

# from django.http.response import JsonResponse
# from rest_framework.parsers import JSONParser 
# from rest_framework import status
 
# from tutorials.models import Tutorial
# from tutorials.serializers import TutorialSerializer
# from rest_framework.decorators import api_view

# Create your views here.

# HOME_HTML = """

#     <h1> Webpage Home </h1>

#     <div>
#     <p> Welcome to the webpage home! </p>
#     </div>

# """

# PROD_HTML = """

#     <h1> View Products Page </h1>

#     <div>
#     <p> Welcome to the View Products Page! </p>
#     </div>

# """

# dummy data for home view testing

products = [

    {
        'name': 'Apple MacBook Pro',
        'price': '$1500',
        'available_units': '5',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
        'seller': 'Apple'
    },
    {
        'name': 'Apple iPad',
        'price': '$1250',
        'available_units': '3',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
        'seller': 'Apple'
    },
    {
        'name': 'Apple iPhone',
        'price': '$1000',
        'available_units': '1',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
        'seller': 'Apple'
    }

]

def home(request):
    # return HttpResponse(HOME_HTML)
    return render(request, 'base/home.html')

def product_page(request):

    # return HttpResponse(PROD_HTML)

    queryset = Product.objects.all()
    product_obj = Product.objects.get(id=1)

    product_context = {
        "product_list": queryset,
        "name": product_obj.name,
        "price": product_obj.price,
        "available_units": product_obj.description,
        "seller": product_obj.seller
    }

    return render(request, 'base/prod-view.html', product_context)

# @api_view(('GET',))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def get(request):
#         queryset = Product.objects.all()
#         product_obj = Product.objects.get(id=1)

#         product_context = {
#             "product_list": queryset,
#             "name": product_obj.name,
#             "price": product_obj.price,
#             "available_units": product_obj.description,
#             "seller": product_obj.seller
#         }
#         return render(request, 'base/prod-list.html', product_context)