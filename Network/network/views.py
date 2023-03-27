import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User, Post, Like

@csrf_exempt
@login_required
def add(request):

    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    data = json.loads(request.body)
    body = data.get('body', "")

    post = Post(
        user = request.user,
        body = body
    )
    print(post)
    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)

@csrf_exempt
@login_required
def like(request, post_id):

    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    post =  Post.objects.get(id=post_id)
    like = Like(user = request.user, post = post)
    like.save()
    print(like)
    post.likes.add(like)
    post.save()

    return JsonResponse({"message": "Post was liked successfully."}, status=201)

@csrf_exempt
@login_required
def unlike(request, post_id):
    print(request.method)
    #if request.method != 'POST':
    #    return JsonResponse({'error': 'POST request required'}, status=400)
    post =  Post.objects.get(id=post_id)
    toRemove = Like.objects.get(user=request.user, post=post)
    post.likes.remove(toRemove)
    toRemove.delete()

    return JsonResponse({"message": "Post unliked successfully."}, status=201)

@login_required
def get_post(request, post_id):
    toReturn = Post.objects.get(id=post_id)

    return JsonResponse(toReturn.serialize(), safe=False)

@csrf_exempt
@login_required
def edit(request, post_id):

    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    data = json.loads(request.body)
    body = data.get('body', "")

    post = Post.objects.get(id=post_id)
    post.body = body
    print(post)
    post.save()

    return JsonResponse({"message": "Post edited successfully."}, status=201)

def viewpage(request, page):

    posts = []
    print(page)
    # Filter emails returned based on mailbox
    if page == "all":
        posts = Post.objects.all()
    elif page == "following":
        posts = Post.objects.filter(user__in=request.user.following.all())
    else:
        print("smile")
        users = User.objects.all()
        
        for user in users:
            if user.username == page:
                foundUser = user
        print("found the user!")
        print(foundUser)
        posts = Post.objects.filter(user=foundUser)
    
    print(len(posts))
    
    # Return emails in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator([post.serialize() for post in posts], 10)
    postPages = []
    print(paginator.page_range)
    for i in paginator.page_range:
        print(paginator.page(i).object_list)
        postPages.append(paginator.page(i).object_list)
    return JsonResponse(postPages, safe=False)

def index(request):
    return render(request, "network/index.html")

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def follow(request, profile):
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    request.user.following.add(User.objects.get(username=profile))
    request.user.save()

    return JsonResponse({"message": "Successfully followed!"}, status=201)

@csrf_exempt
@login_required
def unfollow(request, profile):

    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    request.user.following.remove(User.objects.get(username=profile))

    return JsonResponse({"message": "Successfully unfollowed!"}, status=201)

@login_required
def is_following(request, profile):
    print(request.method)
    if request.user.username == profile:
        return JsonResponse({"following": 'same'}, status=201, safe=False)

    for user in request.user.following.all():
        if user.username == profile:
            return JsonResponse({"following": True}, status=201, safe=False)

    return JsonResponse({"following": False}, status=201, safe=False)

@login_required
def have_liked(request, post_id):

    for like in Post.objects.get(id=post_id).likes.all():
        if like.user == request.user:
            return JsonResponse({"liked": True}, status=201, safe=False)

    return JsonResponse({"liked": False}, status=201, safe=False)