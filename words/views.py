from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Base, UserWord
from random import randint
import datetime
from django.utils import timezone
from time import sleep
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from math import ceil


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

@check_login
def index(request):
    if request.method == 'POST' and ('id' in request.POST):
        if not(UserWord.objects.filter(user_id_id=request.session['id'], word_id_id = int(request.POST['id']))):
            uw = UserWord(user_id_id=request.session['id'], word_id_id = int(request.POST['id']))
            uw.save()
    elif request.method == 'POST' and ('search' in request.POST):
        words = []
        idxs = []
        ws = Base.objects.filter(word_eng__startswith=request.POST['search'])[:5]
        for word in ws:
            idxs.append(word.id)
            words.append(word.word_eng + " - " + word.word_rus)
        content = {"words": words, "idxs": idxs}
        return render(request, 'words/index.html', content)
    n = 8050
    words = []
    idxs = []
    for i in range(5):
        idx = randint(1, n)
        idxs.append(idx)
        word = Base.objects.filter(id=idx)[0]
        words.append(word.word_eng + " - " + word.word_rus)
    now = timezone.now()
    words_to_train = len(UserWord.objects.filter(user_id_id=request.session['id'], when_to_train__lte=now))
    content = {"words": words, "idxs": idxs, "totrain": words_to_train}
    return render(request, 'words/index.html', content)

@check_login
def add(request):
    if request.method == 'POST' and ('id' in request.POST):
        if not(UserWord.objects.filter(user_id_id=request.session['id'], word_id_id = int(request.POST['id']))):
            uw = UserWord(user_id_id=request.session['id'], word_id_id = int(request.POST['id']))
            uw.save()
    return redirect("/words/")

@check_login
def train(request):
    now = timezone.now()
    user_words = UserWord.objects.filter(user_id_id=request.session['id'], when_to_train__lte=now)[:5]
    idxs = list(map(lambda x: x.word_id_id, user_words))
    words = list(map(lambda x: Base.objects.filter(id=x)[0], idxs))
    content = {"engWords": [words[i].word_eng for i in range(len(words))],
               'rusWords': [word.word_rus for word in words],
               "idxs": idxs }
    return render(request, 'words/train1.html', content)

@check_login
def mywords(request):
    if request.method == 'POST':
        UserWord.objects.filter(user_id_id=request.session['id'], word_id_id=int(request.POST['id'])).delete()
    words = []
    idxs = []
    times = []
    nextTrain = []
    ws = UserWord.objects.filter(user_id_id=request.session['id'])
    for word2 in ws:
        idxs.append(word2.word_id_id)
        word = Base.objects.filter(id=word2.word_id_id)[0]
        words.append(word.word_eng + " - " + word.word_rus)
        times.append(word2.count)
        delta = word2.when_to_train - timezone.now()
        nextTrain.append(delta.days)
    content = {"words": words, "idxs": idxs, "times" : times, "nexts": nextTrain}
    return render(request, 'words/mywords.html', content)

@check_login
def fetch(request):
    words = []
    idxs = []
    ws = UserWord.objects.filter(user_id_id=request.session['id'])
    for word2 in ws:
        idxs.append(word2.word_id_id)
        word = Base.objects.filter(id=word2.word_id_id)[0]
        words.append(word.word_eng + " - " + word.word_rus)
    content = {"words": words, "idxs": idxs}
    return JsonResponse(content)

@check_login
def finish(request):
    if request.method == "POST":
        a = str(request.read()).split(",")
        a[0] = a[0][3:]
        a[-1] = a[-1][:len(a[-1])-2]
        for word in a:
            w, c = word.split(":")
            c = int(c)
            w = int(w[1:-1])
            b = UserWord.objects.filter(user_id_id=request.session['id'], word_id_id=w)[0]
            b.train(c == 0)
            b.save()

    return HttpResponse("apchi")

