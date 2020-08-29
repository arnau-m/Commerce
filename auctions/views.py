from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Bids, Comments, Whatchlist


def index(request):
    header = "Active Listings"
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all(),
        "header": header
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, title):
    listing = Listings.objects.get(title = title)
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "listing": listing
        })

def categories(request):
    categoriesDic = []
    listings = Listings.objects.all()
    for i in listings:
        if i.category not in categoriesDic:
            categoriesDic.append(i.category)

    return render (request, "auctions/categories.html", { "categories": categoriesDic })


def viewCategory(request, category):
    allLists = Listings.objects.all()
    selectedLists = []
    for i in allLists:
        if i.category == category:
            selectedLists.append(i)

    return render(request,"auctions/index.html",{"listings":selectedLists, "header":category})
