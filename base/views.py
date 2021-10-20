from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

HOME_HTML = """

    <h1> Webpage Home </h1>

    <div>
    <p> Welcome to the webpage home! </p>
    </div>

"""

PROD_HTML = """

    <h1> View Products Page </h1>

    <div>
    <p> Welcome to the View Products Page! </p>
    </div>

"""

def home(request):
    return HttpResponse(HOME_HTML)

def product_page(request):

    return HttpResponse(PROD_HTML)
