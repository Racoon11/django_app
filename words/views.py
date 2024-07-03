from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Base, UserWord
from random import randint
import datetime
from django.utils import timezone
from time import sleep


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
    content = {"words": words, "idxs": idxs}
    return render(request, 'words/index.html', content)


def train(request):
    now = timezone.now()
    user_words = UserWord.objects.filter(user_id_id=request.session['id'], when_to_train__lte=now)[:5]
    idxs = list(map(lambda x: x.word_id_id, user_words))
    words = list(map(lambda x: Base.objects.filter(id=x)[0], idxs))
    for i in range(len(words)):
        return train1(request, words[i])
    return HttpResponse("done")


def train1(request, word):
    print('here')
    content = {'engWord': word.word_eng,
               'rusWords1': [word.word_rus, 'слово2оооо'],
               'rusWords2': ['слово3', 'слово4']}
    return render(request, 'words/train1.html', content)



def mywords(request):
    if request.method == 'POST':
        UserWord.objects.filter(user_id_id=request.session['id'], word_id_id = int(request.POST['id'])).delete()
    words = []
    idxs = []
    ws = UserWord.objects.filter(user_id_id=request.session['id'])
    for word2 in ws:
        idxs.append(word2.word_id_id)
        word = Base.objects.filter(id=word2.word_id_id)[0]
        words.append(word.word_eng + " - " + word.word_rus)
    content = {"words": words, "idxs": idxs}
    return render(request, 'words/mywords.html', content)

