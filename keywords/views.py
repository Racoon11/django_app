from django.shortcuts import render, Http404
import spacy
import pytextrank
import nltk
from django.contrib.auth.models import User
from django.http import HttpResponse
from translatepy import Translator

from nltk.corpus import stopwords
from words.models import BaseEng, UserWordEng, BaseGerm, UserWordGerm
from .models import CheckWordsEng, CheckWordsGer
import re

nlp_ger = spacy.load('de_core_news_sm')
nlp_eng = spacy.load('en_core_web_sm')

nlp_ger.add_pipe("textrank")
nlp_eng.add_pipe("textrank")

german_stop_words = stopwords.words('german')
english_stop_words = stopwords.words("english")


def check_on_user(request):
    try:
        user = User.objects.filter(id=request.session['id'])[0]
    except (KeyError):
        return False
    else:
        return user


def check_login(func):
    def wrapper(req):
        if not check_on_user(req):
            return HttpResponse("We don't know u")
        return func(req)

    return wrapper


def check_admin(func):
    def wrapper(req):
        user = check_on_user(req)
        if not user or not user.is_superuser:
            return HttpResponse("We don't know u")

        return func(req)

    return wrapper


def keywords(text, nlp, n=10):
    doc = nlp(text)
    keys = []
    for phrase in doc._.phrases[:n]:
        keys.append(phrase.text)
    return keys


def lemm(words, nlp, stop_words):
    ans = set()
    for i in words:
        words_nlp = nlp(i)
        sep = [j.lemma_ for j in words_nlp if j.lemma_ not in stop_words]
        rem = [re.sub(r'[^\w\s]', '', token) for token in sep]
        rem = [re.sub(r'[0-9]', '', token) for token in rem]
        rem = [token for token in rem if token]
        ans |= set(rem)
    return ans


Base = BaseEng
UserBase = UserWordEng
CheckWords = CheckWordsEng


def check_words(words):
    ans = {word: "check" for word in words}
    trans = {word: "none" for word in words}
    ids = {word: "none" for word in words}
    for word in words:
        base_word = Base.objects.filter(word_eng=word).first()
        if base_word:
            ans[word] = 'base'
            trans[word] = base_word.word_rus
            ids[word] = str(base_word.id)
            user_word = UserBase.objects.filter(word_id=base_word.id)
            if user_word:
                ans[word] = 'user'
        else:
            cw = CheckWords(word_eng=word)
            cw.save()
    return ans, trans, ids


@check_login
def index(request):
    global Base, UserBase, CheckWords
    content = {}
    text = ''

    if request.method == "POST":
        if len(request.FILES) != 0:
            text = str(request.FILES['formFile'].file.getvalue())
        elif request.POST['textarea']:
            content['text'] = request.POST['textarea']
            text = request.POST['textarea']
        if text:
            if 'lang' in request.session and request.session['lang'] == 'ger':
                nlp = nlp_ger
                stopwords = german_stop_words
                Base = BaseGerm
                UserBase = UserWordGerm
                CheckWords = CheckWordsGer
            else:
                nlp = nlp_eng
                stopwords = english_stop_words
                Base = BaseEng
                UserBase = UserWordEng
                CheckWords = CheckWordsEng
            keys = lemm(keywords(text, nlp), nlp, stopwords)
            checked, trans, ids = check_words(keys)
            content['words'] = checked
            content["trans"] = trans
            content["ids"] = ids
            return render(request, "keywords/list.html", content)
    return render(request, "keywords/index.html", content)


@check_login
def add(request):
    if request.method == "POST":
        n = 0
        for key in list(request.POST.keys())[1:-1]:
            word_id = request.POST[key]
            if not (UserBase.objects.filter(user_id_id=request.session['id'], word_id_id=int(word_id))):
                uw = UserBase(user_id_id=request.session['id'], word_id_id=int(word_id))
                uw.save()
                n += 1
        return render(request, "keywords/add.html", {"n": n})
    raise Http404()


@check_admin
def admin_words(request):
    if request.method == "POST":
        data = request.body.decode('utf-8')[1:-1].split(",")
        data_dict = {}
        for var in data:
            key, values = var.split(":")
            data_dict[key[1:-1]] = values[1:-1]

        word_id = data_dict['word_id']
        word = CheckWords.objects.get(id=word_id)
        if data_dict["operation"] == "add":
            word_base = Base(word_eng=data_dict["word_eng"], word_rus=data_dict["word_rus"])
            word_base.save()
        word.delete()

    translator = Translator()
    content = {}
    words = []
    translations = []
    ids = []
    for word in CheckWords.objects.all():
        words.append(word.word_eng)
        if word.word_rus == "none":
            word.word_rus = translator.translate(word.word_eng, "Russian")  # add source_language
            word.save()
        translations.append(word.word_rus)
        ids.append(str(word.id))
    content["words"] = words
    content['trans'] = translations
    content["ids"] = ids

    return render(request, "keywords/admin.html", content)
