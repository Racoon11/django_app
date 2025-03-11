from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from django.http import Http404

from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.core.mail import send_mail

from django.conf import settings
from django.middleware import csrf
from words.models import BaseEng, UserWordEng, BaseGerm, UserWordGerm

from .models import Information
from random import randint
import requests


host = 'http://127.0.0.1:8000'
Base = BaseEng
UserWord = UserWordEng

def check_on_user(request):
    try:
        user = User.objects.filter(id=request.session['id'])[0]
    except (KeyError):
        return False
    else:
        return True


def check_login(func):
    def wrapper(req):
        if not check_on_user(req):
            return HttpResponse("We don't know u")
        return func(req)

    return wrapper


def registration(request):
    if check_on_user(request):
        raise Http404("You are logged in")
    if request.method == 'POST':
        content = {}
        if User.objects.filter(email=request.POST["email"]):
            content["email"] = True
        if User.objects.filter(username=request.POST["userName"]):
            content["usernn"] = True
        if content:
            return render(request, "users/registration.html", content)

        request.session["userName"] = request.POST["userName"]
        request.session["email"] = request.POST["email"]
        request.session["password"] = request.POST["password"]
        request.session["firstName"] = request.POST["firstName"]
        request.session["lastName"] = request.POST["lastName"]
        request.session['code'] = ''.join([str(randint(0, 9)) for _ in range(6)])

        send_email([request.POST["email"]], request.session['code'])
        return render(request, "users/code.html")
    return render(request, "users/registration.html")


def save_user(source):
    user = User.objects.create_user(source["userName"], source["email"], source["password"])
    user.first_name = source["firstName"]
    user.last_name = source['lastName']
    user.save()
    inf = Information(user=user, level='Beginner')
    inf.save()


def code(request):
    if (request.POST['code'] == request.session['code']):
        save_user(request.session)
        request.session.flush()
        return HttpResponseRedirect("/users/login")
    return render(request, "users/code.html")


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
            request.session['lang'] = "eng"
            context = {"username": user.username,
                       'lastname': user.last_name,
                       'firstname': user.first_name,
                       'email': user.email}
            return HttpResponseRedirect("/users")
        else:
            return render(request, "users/login.html", {'error': True})
    return render(request, "users/login.html")


@check_login
def index(request):
    try:
        user = User.objects.filter(id=request.session['id'])[0]
        inf = Information.objects.filter(user_id=request.session['id'])[0]
        context = {"username": user.username,
                   'lastname': user.last_name,
                   'firstname': user.first_name,
                   'email': user.email,
                   'level': inf.level,
                   'words': inf.words,
                   'lang': request.session['lang']}
    except KeyError:
        return HttpResponse("We don't know u")
    else:
        return render(request, "users/index.html", context)


def logout(request):
    try:
        request.session.flush()
    except KeyError:
        return render(request, "users/login.html", {'logout': False})
    else:
        return render(request, "users/login.html", {'logout': True})


def send_email(email, text):
    send_mail(
        "LangLand message ^~^",
        text,
        settings.EMAIL_HOST_USER,
        recipient_list=email,
        fail_silently=False, )


@check_login
def edit(request):
    if request.method == 'POST':
        user = User.objects.filter(id=request.session['id'])[0]
        inf = Information.objects.filter(user_id=request.session['id'])[0]
        if request.POST['firstName'] != "":
            user.first_name = request.POST['firstName']
        if request.POST['lastName'] != "":
            user.last_name = request.POST['lastName']
        if request.POST['level'] != "":
            inf.level = request.POST['level']
        if request.POST['lang'] != (request.session['lang'] if 'lang' in request.session else 'eng'):
            requests.get(host + '/words/language?language='+request.POST['lang'])
            request.session['lang'] = request.POST['lang']
        user.save()
        inf.save()
        return HttpResponseRedirect("/users")
    try:
        user = User.objects.filter(id=request.session['id'])[0]
        inf = Information.objects.filter(user_id=request.session['id'])[0]
        context = {
            'lastname': user.last_name,
            'firstname': user.first_name,
            'level': inf.level,
            'lang': request.session['lang'] if 'lang' in request.session else "eng"}
    except KeyError:
        return HttpResponse("We don't know u")
    return render(request, "users/edit.html", context)
