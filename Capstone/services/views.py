import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal

from .models import User, Job, Message

# Create your views here.
def index(request):
    return render(request, 'services/index.html')


def get_jobs(request):
    print(34)    
    jobs = Job.objects.filter(buyer=None).exclude(user=request.user)
    
    return JsonResponse([job.serialize() for job in jobs], safe = False)

@csrf_exempt
def create_job(request):
    print(request.method)
    if request.method != "POST":

        return JsonResponse({"error" : "POST request required"}, status=400)

    data = json.loads(request.body)
    
    job = Job(
        user=request.user,
        price = Decimal(data.get("price", "")),
        description = data.get("description", ""),
        buyer=None
    )

    job.save()

    return JsonResponse({"message" : "Application posted successfully."}, status=201)

@csrf_exempt
def hire(request, job_id):

    if request.method != "POST":
        return JsonResponse({"error" : "POST request required"}, status=400)

    job = Job.objects.get(id=job_id)
    job.buyer = request.user
    job.save()

    return JsonResponse({"message" : "Hire successful!"}, status=201)

def get_senders(request):

    senders = []

    for message in Message.objects.all():
        if message.sender.username not in senders:
            senders.append(message.sender.username)

    return JsonResponse(senders, safe = False)

def get_msgs(request, other_user):

    received = Message.objects.filter(receiver=request.user, sender=User.objects.get(username=other_user))
    sent = Message.objects.filter(receiver=User.objects.get(username=other_user), sender=request.user)

    fullMsgs = received.union(sent)
    
    fullMsgs = fullMsgs.order_by("-timestamp").all()

    return JsonResponse([msg.serialize() for msg in fullMsgs], safe = False)

@csrf_exempt
def send_msg(request, other_user):

    if request.method != "POST":
        return JsonResponse({"error" : "POST request required"}, status=400)
    
    data = json.loads(request.body)
    
    print(request.user)
    print(User.objects.get(username=other_user))

    msg = Message(
        sender=request.user,
        text=data.get("text", ""),
        receiver=User.objects.get(username=other_user)
    )

    msg.save()

    return JsonResponse({"message": "Message successfully sent!"}, status=201)

def get_olds(request):

    jobs = Job.objects.filter(buyer=request.user)

    return JsonResponse([job.serialize() for job in jobs], safe = False)

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
            return render(request, "services/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "services/login.html")

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
            return render(request, "services/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "services/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "services/register.html")
