from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import F
from django.urls import reverse
from django.views import generic

from django.contrib.auth.models import User

from django.contrib.auth import authenticate

def registration(request):
    #template = loader.get_template("users/registration.html")
    if request.method == 'POST':
        if (User.objects.filter(email = request.POST["email"])):
            return HttpResponseRedirect(reverse('users:email_exists'))
        user = User.objects.create_user(request.POST["userName"], request.POST["email"], request.POST["password"])
        user.first_name = request.POST["firstName"]
        user.last_name = request.POST['lastName']
        user.save()
        print(user.last_name)
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/registration.html")


def email_exists(request):
    return HttpResponse("email already exists")

def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            request.session['username'] = user.username
            request.session['id'] = user.id
            context = {"username": user.username,
                        'lastname': user.last_name,
                       'firstname': user.first_name,
                       'email': user.email}
            return render(request, "users/index.html", context)
    return render(request, "users/login.html", {'logout': False})

def index(request):
    try:
        user = User.objects.filter(id = request.session['id'])[0]
        print(user)
        context = {"username": user.username,
                   'lastname': user.last_name,
                   'firstname': user.first_name,
                   'email': user.email}
    except (KeyError):
        return HttpResponse("We don't know u")
    else:
        return render(request, "users/index.html", context)

