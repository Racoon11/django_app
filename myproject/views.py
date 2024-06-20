
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


def index(request):
    try:
        context = {'login': True,
                   'username': request.session['username']}
    except (KeyError):
        return render(request, "myproject/index.html")
    return render(request, "myproject/index.html", context)
