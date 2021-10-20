from django.shortcuts import render
from django.http import HttpResponse

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

    context = {
        'products': products
    }

    return render(request, 'base/prod-view.html', context)
