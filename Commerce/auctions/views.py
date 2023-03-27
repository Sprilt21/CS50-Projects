from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm
from .models import User, Comment, Bid, Listing
from django import forms

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "startingBid", "image", "category"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]

class WatchForm(ModelForm):
    listing = forms.CharField(label="Listing", widget=forms.HiddenInput())    

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

def createListing(request):

    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = Listing(
                title=form.cleaned_data['title'],
                description =form.cleaned_data['description'], 
                startingBid=form.cleaned_data['startingBid'],
                image=form.cleaned_data['image'],
                category=form.cleaned_data['category'],
                user = request.user)
            request.user.made.append(listing.title)
            listing.save()
            request.user.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
        return render(request, 'auctions/add.html', {
            "form" : ListingForm()
        })

def viewListing(request, name):

    listing = Listing.objects.get(title=name)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(id=Comment.objects.count()+1, comment=form.cleaned_data['comment'])
            comment.listing = listing
            comment.save()
        return HttpResponseRedirect(reverse('item', kwargs={'name' : name}))
    
    comments = Comment.objects.all().filter(listing=listing)

    return render(request, 'auctions/listing.html', {
        "listing" : listing,
        "form" : CommentForm,
        "comments" : comments
    })

def categories(request):

    categories = Listing.objects.all().values('category').distinct()
    uniques = []

    for category in categories:
        if not category == "" and not category == None:
            uniques.append(category['category'])

    return render(request, 'auctions/categories.html', {
        "categories" : uniques
    })

def category(request, category):

    listings = Listing.objects.all().filter(category=category)
    
    return render(request, 'auctions/category.html', {
        "category" : category,
        "listings" : listings
    })

def makeBid(request, name):

    listing = Listing.objects.get(title=name)

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():

            bid = Bid(id=Bid.objects.count()+1, amount=form.cleaned_data['amount'])
            bid.save()

            if form.cleaned_data['amount'] > listing.startingBid:
                listing.startingBid = form.cleaned_data['amount']
                listing.save()
                listing.currentWinner = request.user.username

                comments = Comment.objects.all().filter(listing=listing)
                
                return redirect('/listing/' + name, {
                    "listing" : Listing,
                    "form" : CommentForm,
                    "comments" : comments
                })
    else:
        return render(request, 'auctions/bid.html', {
            "form" : BidForm,
            "listing" : listing
        })

def addToWatch(request, name):

    listing = Listing.objects.get(title=name)
    request.user.watchlist.append(listing.title)
    comments = Comment.objects.all().filter(listing=listing)

    return redirect('/listing/' + name, {
        "listing" : listing,
        "form" : CommentForm,
        "comments" : comments
    })

def watchList(request):
    
    listings = []

    for name in request.user.watchlist:
        listings.append(Listing.objects.get(title=name))
    
    return render(request, 'auctions/watchlist.html', {
        "watchlist" : listings
    })

def close(request, name):

    listing = Listing.objects.get(title=name)
    
    winner = User.objects.all().filter(username=listing.currentWinner)
    listing.closed = True
    if len(winner) > 0:
        winner[0].won.append(listing.title)
        winner[0].save()

    return redirect('/listing/' + name, {
        "listing" : listing,
        "form" : CommentForm,
        "comments" : Comment.objects.all().filter(listing=listing)
    })