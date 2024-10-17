from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from users.models import Information
from words.models import BaseEng

def check_on_user(request):
    try:
        user = User.objects.filter(id=request.session['id'])[0]
        return user.is_superuser
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

@check_login
def index(request):
    get_info(Information)
    return render(request, 'base/index.html')

def get_info(table):
    obj = table.objects.all()
    columns = table._meta.fields
    ans = {}
    for field in table._meta.fields:
        ans[field] = []

    for i in obj:
        print(i)
