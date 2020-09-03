from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User, Listings, Bids, Comments, Watchlist


def index(request):
    header = "Active Listings"
    listings = Listings.objects.filter(status = True)
    return render(request, "auctions/index.html",{"listings":listings,"check": True, "header":"Active Listings"})


def closed(request):
    listing = Listings.objects.filter(status = False)
    return render(request, "auctions/index.html" ,{"listings":listing, "check": False, "header":"Closed Listings"})

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
    list = Listings.objects.get(title = title)
    if request.method == "GET":
        if list.status == True:
            bids = Bids.objects.filter(listing = list)
            comment = Comments.objects.filter(listing = list)
            if comment:
                return render(request,"auctions/listing.html",{"listing":list,"bids":bids,"comments":comment})
            return render(request,"auctions/listing.html",{"listing":list,"bids":bids})
        return render(request,"auctions/closedlisting.html",{"listing":list})

    #if Method is POST means comment added request made
    comment = request.POST.get("comment")
    add_comment = Comments(username = request.user.username,comment = comment,listing = list)
    add_comment.save()
    return render(request,"auctions/message.html",{"message": "Comment Added!"})

def categories(request):
    categoriesDic = []
    listings = Listings.objects.all()
    for i in listings:
        if i.category not in categoriesDic:
            categoriesDic.append(i.category)

    return render (request, "auctions/categories.html", { "categories": categoriesDic })


def viewCategory(request, category):
    allLists = Listings.objects.filter(status = True)
    selectedLists = []
    for i in allLists:
        if i.category == category:
            selectedLists.append(i)

    return render(request,"auctions/index.html",{"listings":selectedLists, "header":category})

def watchlist(request):
    username = request.user.username
    ids = []
    selected = []
    listings = Watchlist.objects.values_list('listing',flat = True).filter(username = username)
    for i in listings:
        ids.append(i)

    for j in ids:
        list = Listings.objects.get(pk = j)
        selected.append(list)
    return render(request, "auctions/watchlist.html" ,{"listings":selected, "header":"Your Watchlist"})

def addWatchlist(request, title):
    listing = Listings.objects.get(title = title)
    username = request.user.username
    listings = Watchlist.objects.values_list('listing',flat = True).filter(username = username)
    for i in listings:
        if listing.id == i:
            return render(request, "auctions/message.html",{"message": "Already added to Watchlist!"})
    watchlist = Watchlist(username = username , listing = listing)
    watchlist.save()
    return render(request, "auctions/message.html", {"message":"Added to Watchlist"})

def deletewatchlist(request, title):
    username = request.user.username
    list = Listings.objects.get(title = title)
    toDeleteList = Watchlist.objects.get(username = username, listing_id = list.id).delete()
    return render(request,"auctions/message.html",{"message": "Deleted from Watchlist!"})

def bid(request,title):
    listing = Listings.objects.get(title = title)
    price = int(float(request.POST.get("bid")))
    if price < listing.price:
        return render(request,"auctions/message.html",{"message": "Bid Must be Greater then current price."})

    #if bid value is valid
    listing.price = price
    listing.save()
    username = request.user.username
    bid = Bids(username = username, listing = listing, bid = price )
    bid.save()
    return render(request,"auctions/message.html",{"message": "Your bid Has been Placed."})

def close(request,title):
    list = Listings.objects.get(title = title)
    list.status = False
    highBid = Bids.objects.all().aggregate(max_bid=(Max("bid")))
    bider = Bids.objects.get(bid = highBid['max_bid'])
    list.winner = bider.username
    list.save()
    return render(request,"auctions/message.html",{"message": "Listing Has Been closed!"})

def createListing(request):
    if request.method == "GET":
        return render(request, "auctions/createListing.html")

    title = request.POST.get("title")
    alldata = Listings.objects.all()
    message = "This Listing is Allreay in Use."
    for data in alldata:
        if data.title == title:
            return render(request, "auctions/message.html", {"message":message})
    price = int(request.POST.get("price"))
    description = request.POST.get("description")
    image = request.POST.get("image")
    category = request.POST.get("category")
    username = request.user.username
    #add information to db
    add = Listings(title=title, price=price, description=description, image=image, category=category, owner=username, status=True)
    add.save()
    list = Listings.objects.get(title=title)
    return render(request, "auctions/listing.html", {"listing":list})
