from typing import List
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, request

from base.forms import UserProfileForm
from .models import CartProduct, Product, Category, Rating, Cart, CartProduct, ReviewProduct, UserProfile, Wishlist
from django.db.models import Q
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as log_out
from urllib.parse import urlencode
from django.conf import settings
from django.http import HttpResponseRedirect
import json
from django.views.generic import DetailView, ListView
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.template.response import TemplateResponse

from base import models

"""
Sources:
https://www.youtube.com/watch?v=Xjty8q524Jo&list=PLLRM7ROnmA9F2vBXypzzplFjcHUaKWWP5&index=2

"""

# dummy data
# products = [

#     {
#         'name': 'Apple MacBook Pro',
#         'price': '$1500',
#         'available_units': '5',
#         'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
#         'seller': 'Apple'
#     },
#     {
#         'name': 'Apple iPad',
#         'price': '$1250',
#         'available_units': '3',
#         'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
#         'seller': 'Apple'
#     },
#     {
#         'name': 'Apple iPhone',
#         'price': '$1000',
#         'available_units': '1',
#         'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
#         'seller': 'Apple'
#     }

# ]

def home(request):
    
    return render(request, 'base/home.html')


def product_page(request):

    queryset = Product.objects.all()

    context = {
        'queryset': queryset
    }

    return render(request, 'base/prod-view.html', context=context)


class ProductView(ListView):

    model = Product
    template = 'base/product_list.html'

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

            # print("rating = ", prod.ratings.name)

            ratings_list.append(prod.ratings.name)

            average_rating = round((sum(ratings_list) / len(ratings_list)), 2)
        

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
        return render(request, 'base/profile.html')
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
    user_profile_obj = get_object_or_404(UserProfile, user=request.user)
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
        'user_name': user_name,
        'user_profile_obj': user_profile_obj,
    })


def products(request, slug):

    object = get_object_or_404(Product, slug=slug)

    if request.method == "POST":

        rev_content = request.POST.get('review', '')

        print("rev_content:", rev_content)

        review = ReviewProduct.objects.create(product=object, user=request.user, review=rev_content)

        return redirect("base:product", slug=slug)

    review_list = ReviewProduct.objects.filter(product=object)

    # user_meta = UserProfile.objects.filter(user=review_list.user)

    context = {

        "object": object,
        "review_list": review_list,
        # "user_meta": user_meta

    }


    return render(request, "base/product.html", context)

# def add_review(request, slug):

#     new_review_form = ReviewForm(request.POST)

#     if new_review_form.is_valid():

#         new_review = new_review_form.save()


class ProductDetailView(DetailView):

    model = Product
    template_name = "base/product.html"

item_added_to_cart = 0
initial_available_units = 0

@login_required
def add_to_cart(request, slug):
    
    product = get_object_or_404(Product, slug=slug)
    cart_product, created = CartProduct.objects.get_or_create(product=product, 
    user=request.user)
    # print("item units: ", product.available_units)
    global item_added_to_cart
    global initial_available_units

    cart_orders_list = Cart.objects.filter(user=request.user, is_ordered=False)

    if cart_orders_list.exists() == False:

        cart_order = Cart.objects.create(user=request.user)
        initial_available_units = product.available_units
        print("init avail units: ", initial_available_units)
        cart_order.products.add(cart_product)
        product.available_units -= 1
        product.save()
        item_added_to_cart += 1
        messages.info(request, "Created cart and added {0}!".format(product.title))
        return redirect("base:product", slug=slug)

    else:
        
        cart_order = cart_orders_list[0]

        if product.available_units != 0 and cart_order.products.filter(product__slug = product.slug).exists() == False:

            initial_available_units = product.available_units
            print("init avail units: ", initial_available_units)
            cart_order.products.add(cart_product)
            product.available_units -= 1
            product.save()
            item_added_to_cart += 1
            messages.info(request, "Added {0} to your cart!".format(product.title))
            return redirect("base:cart")

        elif product.available_units != 0 and cart_order.products.filter(product__slug = product.slug).exists() == True:

            cart_product.quantity += 1
            cart_product.save()
            product.available_units -= 1
            product.save()
            item_added_to_cart += 1
            messages.info(request, "Added 1 unit of {0} to your cart.".format(product.title))
            return redirect("base:product", slug=slug)

        else:
            messages.info(request, "No more items left to be added to cart. Sorry :(")
            return redirect("base:product", slug=slug)


@login_required
def add_to_wishlist(request, slug):

    product = get_object_or_404(Product, slug=slug)
    wishlist_product, created = CartProduct.objects.get_or_create(product=product, user=request.user)
    wishlist_product_list = Wishlist.objects.filter(user=request.user, added_to_cart=False)

    if wishlist_product_list.exists() == False:

        wishlist = Wishlist.objects.create(user=request.user)
        wishlist.products.add(wishlist_product)
        messages.info(request, "Created wishlist and added {0}!".format(product.title))
        return redirect("base:wishlist")
    
    else:
        wishlist = wishlist_product_list[0]
        wishlist.products.add(wishlist_product)
        messages.info(request, "Added {0} to your wishlist!".format(product.title))
        return redirect("base:product", slug=slug)
    
@login_required
def remove_all_from_cart(request, slug):

    product = get_object_or_404(Product, slug=slug)
    cart_orders_list = Cart.objects.filter(user=request.user, is_ordered=False)
    global item_added_to_cart

    if cart_orders_list.exists() == False:

        messages.info(request, "There's nothing in your cart right now.")
        return redirect("base:product", slug=slug)

    else:

        cart_order = cart_orders_list[0]

        if cart_order.products.filter(product__slug = product.slug).exists() == False:

            messages.info(request, "{0} was not found in your cart.".format(product.title))
            return redirect("base:product", slug=slug)

        else:

            cart_product_to_remove = CartProduct.objects.filter(product=product, user=request.user)[0]
            cart_order.products.remove(cart_product_to_remove)
            product.available_units += item_added_to_cart 
            product.save()
            return_string = "{0} units of {1} were removed from your cart".format(item_added_to_cart, product.title)
            messages.info(request, return_string)
            item_added_to_cart = 0
            return redirect("base:product", slug=slug)   

@login_required
def remove_one_from_cart(request, slug):

    product = get_object_or_404(Product, slug=slug)
    cart_orders_list = Cart.objects.filter(user=request.user, is_ordered=False)
    global initial_available_units
    print("init avail units: ", initial_available_units)
    print("prod avail units: ", product.available_units)
    
    if cart_orders_list.exists() == False:

        messages.info(request, "{0} was not found in your cart.".format(product.title))
        return redirect("base:product", slug=slug)

    else:

        cart_order = cart_orders_list[0]

        if cart_order.products.filter(product__slug = product.slug).exists() == False:

            messages.info(request, "{0} was not found in your cart.".format(product.title))
            return redirect("base:product", slug=slug)

        else:

            cart_product_to_reduce = CartProduct.objects.filter(product=product, user=request.user)[0]

            if cart_product_to_reduce.quantity > 0 and product.available_units <= (initial_available_units - 1):

                cart_product_to_reduce.quantity -= 1
                cart_product_to_reduce.save()
                product.available_units += 1
                product.save()
                return_string = "1 unit of {0} removed from cart".format(product.title)
                messages.info(request, return_string)
                return redirect("base:product", slug=slug)

            else:

                messages.info(request, "{0} was not found in your cart.".format(product.title))
                return redirect("base:product", slug=slug)

@login_required
def cart_view(request):

    try:
        cart = Cart.objects.get(user=request.user, is_ordered=False)
        context = {
            'cart': cart
        }
        # print(cart.products.count())
        request.session['cart_count_num'] = cart.products.count()
        return render(request, "base/cart-view.html", context=context)
        
    except ObjectDoesNotExist:
        messages.error(request, "You haven't created a cart yet.")
        return redirect("base:profile")

def autosuggestion_title(request):

    queryset = Product.objects.filter(title__icontains=request.GET.get('term'))
    title_return_list = []
    for prod in queryset:
        title_return_list.append(prod.title)
    return JsonResponse(title_return_list, safe=False)

@login_required
def wishlist_view(request):

    try:
        wishlist = Wishlist.objects.get(user=request.user)
        context = {
            'wishlist': wishlist,
        }
        request.session['wishlist_count_num'] = wishlist.products.count()
        return render(request, "base/wishlist-view.html", context=context)
        
    except ObjectDoesNotExist:
        messages.error(request, "You haven't created a wishlist yet.")
        return redirect("base:profile")

@login_required
def remove_all_from_cart_add_to_wishlist(request, slug):

    product = get_object_or_404(Product, slug=slug)
    cart_orders_list = Cart.objects.filter(user=request.user, is_ordered=False)
    global item_added_to_cart

    if cart_orders_list.exists() == False:

        messages.info(request, "There's nothing in your cart right now.")
        return redirect("base:product", slug=slug)

    else:

        cart_order = cart_orders_list[0]

        if cart_order.products.filter(product__slug = product.slug).exists() == False:

            messages.info(request, "{0} was not found in your cart.".format(product.title))
            return redirect("base:product", slug=slug)

        else:

            cart_product_to_remove = CartProduct.objects.filter(product=product, user=request.user)[0]
            cart_order.products.remove(cart_product_to_remove)
            product.available_units += item_added_to_cart 
            product.save()
            add_to_wishlist(request, slug)
            return_string = "{0} was removed from your cart!".format(product.title)
            messages.info(request, return_string)
            item_added_to_cart = 0
            return redirect("base:product", slug=slug) 

@login_required
def edit_profile(request):

    user_profile_obj = get_object_or_404(UserProfile, user=request.user)

    user_profile_form = UserProfileForm(request.POST, instance=user_profile_obj)

    if user_profile_form.is_valid():
        new_form = user_profile_form.save()
        return redirect("base:profile")

    context = {
        'form': user_profile_form,
        'user': user_profile_obj
    }

    return render(request, "base/edit-profile.html", context=context)

