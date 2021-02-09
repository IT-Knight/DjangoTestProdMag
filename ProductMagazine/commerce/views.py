import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework import viewsets

from .models import Product, Wishlist, User
from .serializers import ProductModelSerializer, WishlistModelSerializer

# Create your views here.


def home(request):
    home_template = loader.get_template("commerce/home.html")
    context = {}
    return HttpResponse(home_template.render(context, request))
    # return redirect("schema-redoc")


def products(request):
    index_template = loader.get_template("commerce/products.html")

    wishlists = Wishlist.objects.filter(utilizator_id=request.user.id)

    # Create extra attribute for each object in wishlists to make a comparison check in template
    for wishlist in wishlists:
        wishlist.products_ids = wishlist.products.values_list('id', flat=True)

    # Get and set unique_wishers for each product
    products = Product.objects.all()
    for product in products:
        product.unique_wishers = Wishlist.objects.filter(products__id=product.id).values_list('utilizator', flat=True).distinct().count()
        product.save()
        # Заметно притормаживает конечно, но где учат делать скоростные конструкции?

    context = {'products': products, 'wishlists': wishlists}
    return HttpResponse(index_template.render(context, request))


def login_view(request):
    if request.method == "GET":
        return render(request, "commerce/login.html")

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:  # is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "commerce/login.html", {
                "message": "Invalid credentials."
            })


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "commerce/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "commerce/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect('index')
    else:
        return render(request, "commerce/register.html")


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class WishlistsViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistModelSerializer


class WishlistView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        wishlists_template = loader.get_template("commerce/wishlists.html")

        context = {'wishlists': Wishlist.objects.filter(utilizator_id=request.user.id)}
        return HttpResponse(wishlists_template.render(context, request))

    # Create new wishlist by JS fetch-request
    def post(self, request):

        data = json.loads(request.body)
        wishlist_title = data.get('wishlist_title')

        new_wishlist = Wishlist.objects.create(utilizator_id=request.user.id, title=wishlist_title)
        data = {"id": int(new_wishlist.id), "title": str(new_wishlist.title), "user": str(new_wishlist.utilizator_id)}
        return JsonResponse(data)

    # Modify existing wishlist by JS fetch-request
    def put(self, request):

        data = json.loads(request.body)
        product_id = data.pop('product_id')
        product = Product.objects.get(id=product_id)

        for key, value in data.items():
            wishlist_id = key
            to_do = value
            wishlist = Wishlist.objects.get(id=wishlist_id)

            if to_do:
                wishlist.products.add(product)
            else:
                wishlist.products.remove(product)

            wishlist.save()

        return HttpResponse(status=204)

    # Delete a wishlist with all content
    def delete(self, request):
        data = json.loads(request.body)
        wishlist_id = data.get('wishlist_id')

        Wishlist.objects.get(id=wishlist_id).delete()

        return HttpResponse(status=204)




