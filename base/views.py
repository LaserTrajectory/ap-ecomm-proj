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

from thefuzz import fuzz
from thefuzz import process

"""
Sources:
https://www.youtube.com/watch?v=Xjty8q524Jo&list=PLLRM7ROnmA9F2vBXypzzplFjcHUaKWWP5&index=2
https://github.com/justdjango/django-ecommerce
https://towardsdatascience.com/fuzzy-string-matching-in-python-68f240d910fe

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
    
    context = {}

    context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']

    return render(request, 'base/home.html', context=context)


def product_page(request):

    queryset = Product.objects.all()

    context = {
        'queryset': queryset
    }

    context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']

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
    nav_search = request.GET.get('nav_search')
    print("nav search = ", nav_search)

    ratings_list = []
    count = 1
    average_rating = 0

    fuzz_match_title_array = []
    fuzz_match_seller_array = []

    title_list = []
    for prod in queryset:
        title_list.append(prod.title)
    # print("title list:", title_list)
    seller_list = []
    for prod in queryset:
        seller_list.append(prod.seller)
    seller_list = list(set(seller_list))
    print(seller_list)

    # print(type(rating_set))

    if title_contains != '' and title_contains is not None:

        queryset = queryset.filter(title__icontains=title_contains)

    elif nav_search != '' and nav_search is not None:

        queryset = queryset.filter(title__icontains=nav_search)

    elif seller_contains != '' and seller_contains is not None:

        queryset = queryset.filter(seller__icontains=seller_contains)

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

    if title_contains != '' and seller_contains == '':

        fuzz_match_array = []
        fuzz_score_array = []

        title_return_list = []
        for prod in queryset:
            title_return_list.append(prod.title)

        if len(title_return_list) == 0:
            for x in title_list:
                fuzz_score = fuzz.ratio(x, title_contains)
                fuzz_match_array.append([x, fuzz_score])
                fuzz_score_array.append(fuzz_score)

        sorted_fuzz_score_array = sorted(fuzz_score_array, reverse=True)

        print(fuzz_match_array)
        print(sorted_fuzz_score_array)

        for i in fuzz_match_array:

            if i[1] == sorted_fuzz_score_array[0] or i[1] == sorted_fuzz_score_array[1]:

                fuzz_match_title_array.append(i[0])

            else:

                continue
            
    # print("matches: ", fuzz_match_title_array)

    if seller_contains != '' and title_contains == '':

        seller_fuzz_match_array = []
        seller_fuzz_score_array = []

        seller_return_list = []

        for prod in queryset:
            seller_return_list.append(prod.seller)

        print(seller_return_list)

        if len(seller_return_list) == 0:
            for x in seller_list:
                fuzz_score = fuzz.ratio(x, seller_contains)
                seller_fuzz_match_array.append([x, fuzz_score])
                seller_fuzz_score_array.append(fuzz_score)

        sorted_fuzz_score_array_seller = sorted(seller_fuzz_score_array, reverse=True)

        print("sorted:", sorted_fuzz_score_array_seller)

        for i in seller_fuzz_match_array:

            if i[1] == sorted_fuzz_score_array_seller[0] or i[1] == sorted_fuzz_score_array_seller[1]:

                fuzz_match_seller_array.append(i[0])

            else:

                continue

    print("seller array:", fuzz_match_seller_array)

    print("title array: ", fuzz_match_title_array)

    print("this queryset", queryset)

    nav_search_check = 0

    if nav_search is not None and not queryset:

        nav_search_check = 1


    context = {
        'queryset': queryset,
        'category_set': category_set,
        'rating_set': rating_set,
        'fuzz_title_matches': fuzz_match_title_array,
        'fuzz_seller_matches': fuzz_match_seller_array
    }

    context['average_rating'] = average_rating
    context['selected_category'] = category
    context['selected_rating'] = rating
    context['title_search_term'] = title_contains
    context['seller_search_term'] = seller_contains
    context['nav_search_term'] = nav_search
    context['nav_search_check'] = nav_search_check
    context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']

    ratings_list = []
    fuzz_match_title_array = []
    fuzz_match_seller_array = []

    return render(request, "base/search_filter_form.html", context=context)


def autosuggestion_title(request):

    queryset = Product.objects.filter(title__icontains=request.GET.get('term'))

    title_return_list = []
    for prod in queryset:
        title_return_list.append(prod.title)

    # print("title return list:", title_return_list)
    print("search term:", request.GET.get('term'))
    # print("len: ", len(title_return_list))
    
    return JsonResponse(title_return_list, safe=False)

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
    user_profile_obj = UserProfile.objects.get_or_create(user=user)[0]
    ordered_cart = Cart.objects.filter(user=request.user, is_ordered=True)
    current_cart = Cart.objects.filter(user=request.user, is_ordered=False)
    current_wishlist = Wishlist.objects.filter(user=request.user)
    # print(ordered_cart)
    
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }

    user_name = user.first_name

    context = {
        'auth0User': auth0user,
        'userdata': userdata,
        'user_name': user_name,
        'user_profile_obj': user_profile_obj,
    }

    if ordered_cart.exists() == True:

        ordered_products_list = []

        for cart in ordered_cart:

            for prod in cart.products.all():

                ordered_products_list.append(prod) 
        
        context['ordered_products_list'] = ordered_products_list

    if current_cart.exists() == True:

        context['current_cart'] = current_cart[0]

    if current_wishlist.exists() == True:

        print(current_wishlist[0].products.all())

        context['current_wishlist'] = current_wishlist[0]

    context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']

    return render(request, 'base/profile.html', context=context)


def products(request, slug):

    object = get_object_or_404(Product, slug=slug)

    if request.method == "POST":

        rev_content = request.POST.get('review', '')

        # print("rev_content:", rev_content)

        review = ReviewProduct.objects.create(product=object, user=request.user, review=rev_content)

        return redirect("base:product", slug=slug)

    review_list = ReviewProduct.objects.filter(product=object)

    # user_meta = UserProfile.objects.filter(user=review_list.user)

    context = {

        "object": object,
        "review_list": review_list,
        # "user_meta": user_meta

    }

    context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']

    return render(request, "base/product.html", context)

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
            cart_product_to_remove.delete()
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
    # print("init avail units: ", initial_available_units)
    # print("prod avail units: ", product.available_units)
    
    if cart_orders_list.exists() == False:

        messages.info(request, "Your cart does not exist.")
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

                if cart_product_to_reduce.quantity == 0:

                    cart_product_to_reduce.delete()

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
        total_price = 0
        for prod in cart.products.all():
            total_price += (prod.product.price * prod.quantity)

        context['total_price'] = total_price
        context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']
    
        return render(request, "base/cart-view.html", context=context)
        
    except ObjectDoesNotExist:
        request.session['cart_count_num'] = 0
        messages.error(request, "Your cart is empty.")
        return redirect("base:profile")

@login_required
def checkout(request):

    try:
        cart = Cart.objects.get(user=request.user, is_ordered=False)
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            'cart': cart,
            'user': user_profile
        }
        # print(cart.products.count())
        total_price = 0
        for prod in cart.products.all():
            total_price += (prod.product.price * prod.quantity)

        context['total_price'] = total_price

        if request.GET.get('order') == 'order':

            cart.is_ordered = True
            cart.save()
            request.session.cart_count_num = 0
            return redirect("base:order-summary")

        context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']

        return render(request, "base/checkout.html", context=context)

    except ObjectDoesNotExist:
        messages.error(request, "You haven't created a cart yet.")
        return redirect("base:profile")

@login_required
def order_summary(request):

    cart = Cart.objects.filter(user=request.user, is_ordered=True)

    recommendations = Cart.objects.filter(is_ordered=True)

    recomm_prod_list = []

    for x in recommendations:

        for prod in x.products.all():

            recomm_prod_list.append(prod.product.title)

    total_price = 0
    for prod in cart[0].products.all():
        total_price += (prod.product.price * prod.quantity)

    user_profile = UserProfile.objects.get(user=request.user)

    context = {
        'cart': cart[0],
        'user': user_profile
    }

    context['total_price'] = total_price
    context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']

    cart_prod_list = []
    for cart_inst in cart:
        prod_list = cart_inst.products.all()
        for x in prod_list:
            cart_prod_list.append(x.product.title)
    print(cart_prod_list)

    recomm_filtered = recomm_prod_list

    for prod in recomm_prod_list:

        for prod_2 in cart_prod_list:

            if prod == prod_2:

                recomm_filtered.remove(prod)

    context['recomm_filtered'] = recomm_filtered

    return render(request, "base/order-summary.html", context=context)

@login_required
def wishlist_view(request):

    try:
        wishlist = Wishlist.objects.get(user=request.user)

        print(wishlist.products.all())

        all_wishlists = Wishlist.objects.all()

        interest_keys = []
        interest_vals = []

        wishlist_entries = []

        for wishlist in all_wishlists:
            prods = wishlist.products.all()
            for prod in prods:
                wishlist_entries.append(prod.product.title)

        wish_set = set(wishlist_entries)

        for i in wish_set:
            count = 0
            for j in wishlist_entries:

                if i == j:

                    count += 1

            interest_keys.append(i)
            interest_vals.append(count)

        # print(interest_keys)
        # print(interest_vals)

        interest_dict = dict(zip(interest_keys, interest_vals))
        # print(interest_dict)

        context = {
            'wishlist': wishlist,
            'interest_dict': interest_dict
        }
        request.session['wishlist_count_num'] = wishlist.products.count()

        context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']

        return render(request, "base/wishlist-view.html", context=context)
        
    except ObjectDoesNotExist:
        request.session['wishlist_count_num'] = 0
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

    context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']

    return render(request, "base/edit-profile.html", context=context)

@login_required
def my_orders(request):

    user_profile = get_object_or_404(UserProfile, user=request.user)

    carts_ordered = Cart.objects.filter(user=request.user, is_ordered=True)
    print(carts_ordered)

    context = {
        'user': user_profile,
        'carts': carts_ordered
    }

    context['picture'] = request.user.social_auth.get(provider='auth0').extra_data['picture']

    return render(request, "base/my-orders.html", context=context)

