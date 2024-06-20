from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import F
from django.urls import reverse
from django.views import generic

from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.core.mail import send_mail

from django.conf import settings
from .models import Information


def check_on_user(request):
    try:
        user = User.objects.filter(id=request.session['id'])[0]
    except (KeyError):
        return False
    else:
        return True

def registration(request):
    if check_on_user(request):
        raise Http404("You are logged in")
    if request.method == 'POST':
        if (User.objects.filter(email = request.POST["email"])):
            return email_exists(request) # fix
        user = User.objects.create_user(request.POST["userName"], request.POST["email"], request.POST["password"])
        user.first_name = request.POST["firstName"]
        user.last_name = request.POST['lastName']
        user.save()
        inf = Information(id=user, level='Beginner')
        inf.save()
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/registration.html")


def email_exists(request):
    return HttpResponse("email already exists")

def login(request):
    lg = request.GET.get('logout', 0)
    if lg:
        logout(request)
    if check_on_user(request):
        raise Http404("You are logged in")
    if request.method == 'POST':
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            request.session['username'] = user.username
            request.session['id'] = user.id
            context = {"username": user.username,
                        'lastname': user.last_name,
                       'firstname': user.first_name,
                       'email': user.email}
            return HttpResponseRedirect("/users")
        else:
            return render(request, "users/login.html", {'error': True})
    return render(request, "users/login.html")

def index(request):
    try:
        user = User.objects.filter(id=request.session['id'])[0]
        inf = Information.objects.filter(id=request.session['id'])[0]
        context = {"username": user.username,
                   'lastname': user.last_name,
                   'firstname': user.first_name,
                   'email': user.email,
                   'level': inf.level,
                   'words': inf.words}
    except (KeyError):
        return HttpResponse("We don't know u")
    else:
        return render(request, "users/index.html", context)

def logout(request):
    try:
        del request.session['username']
        del request.session['id']
    except (KeyError):
        return render(request, "users/login.html", {'logout': False})
    else:
        return render(request, "users/login.html", {'logout': True})

def send_email(email):
    send_mail(
    "Subject here",
    "Here is the message.",
    settings.EMAIL_HOST_USER,
    recipient_list=email,
    fail_silently=False,)

def edit(request):
    if request.method == 'POST':
        user = User.objects.filter(id=request.session['id'])[0]
        inf = Information.objects.filter(id=request.session['id'])[0]
        if request.POST['firstName'] != "":
            user.first_name = request.POST['firstName']
        if request.POST['lastName'] != "":
            user.last_name = request.POST['lastName']
        if request.POST['level'] != "":
            inf.level = request.POST['level']
        user.save()
        inf.save()
        return HttpResponseRedirect("/users")
    try:
        user = User.objects.filter(id=request.session['id'])[0]
        inf = Information.objects.filter(id=request.session['id'])[0]
        print(inf.level)
        context = {
                   'lastname': user.last_name,
                   'firstname': user.first_name,
                   'level': inf.level,}
    except (KeyError):
        return HttpResponse("We don't know u")
    return render(request, "users/edit.html")
