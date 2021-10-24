from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category, Rating
from django.db.models import Q
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from urllib.parse import urlencode
from django.conf import settings
from django.http import HttpResponseRedirect
import json

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
        "title": product_obj.title,
        "price": product_obj.price,
        "available_units": product_obj.description,
        "seller": product_obj.seller,
        "categories": product_obj.categories,
    }

    return render(request, 'base/prod-view.html', product_context)

def SearchFilterView(request):

    queryset = Product.objects.all()
    category_set = Category.objects.all()
    rating_set = Rating.objects.all().order_by('name')
    title_contains = request.GET.get('title_contains')
    seller_contains = request.GET.get('seller_contains')
    id_exact = request.GET.get('id_exact')
    name_or_seller = request.GET.get('name_or_seller')
    view_price_min = request.GET.get('view_price_min')
    view_price_max = request.GET.get('view_price_max')
    category = request.GET.get('category')
    rating = request.GET.get('rating')

    ratings_list = []
    count = 1
    average_rating = 0

    # print(type(rating_set))

    if title_contains != '' and title_contains is not None:

        queryset = queryset.filter(title__icontains=title_contains)

    elif seller_contains != '' and seller_contains is not None:

        queryset = queryset.filter(seller__icontains=seller_contains)

    elif id_exact != '' and id_exact is not None:

        queryset =  queryset.filter(id=id_exact)

    elif name_or_seller != '' and name_or_seller is not None:

        queryset = queryset.filter(Q(title__icontains=name_or_seller) | 
        Q(seller__icontains=name_or_seller)).distinct()

    if view_price_min != '' and view_price_min is not None:

        queryset = queryset.filter(price__gte=view_price_min)

    if view_price_max != '' and view_price_max is not None:

        queryset = queryset.filter(price__lt=view_price_max)

    if category != '' and category is not None and category != 'Choose...':

        queryset = queryset.filter(categories__name=category)

        for prod in queryset:

            print("rating = ", prod.ratings.name)

            ratings_list.append(prod.ratings.name)

            average_rating = sum(ratings_list) / len(ratings_list)
        

    if rating != '' and rating is not None and rating != 'Choose...':

        queryset = queryset.filter(ratings__name=rating)

    context = {
        'queryset': queryset,
        'category_set': category_set,
        'rating_set': rating_set,
    }

    context['average_rating'] = average_rating
    context['selected_category'] = category
    context['selected_rating'] = rating

    ratings_list = []

    return render(request, "base/search_filter_form.html", context=context)


def index(request):
    user = request.user
    if user.is_authenticated:
        return redirect(profile)
    else:
        return render(request, 'base/index.html')

def logout(request):
    log_out(request)
    return_to = urlencode({"returnTo": request.build_absolute_uri("/")})
    logout_url = "https://{}/v2/logout?client_id={}&{}".format(
        settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to,
    )
    return HttpResponseRedirect(logout_url)

@login_required
def profile(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }

    user_name = user.first_name

    return render(request, 'base/profile.html', {
        'auth0User': auth0user,
        'userdata': userdata,
        'user_name': user_name
    })

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