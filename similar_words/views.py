from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
import numpy as np
import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel
from words.models import BaseEng, UserWordEng, BaseGerm, UserWordGerm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier

base_eng_txt = list(map(lambda x: x.word_eng, BaseEng.objects.all()))
base_ger_txt = ""

base_txt = base_eng_txt
Base = BaseEng
UserWord = UserWordEng
dim = 768


class myKNN:

    def __init__(self, user_dict, knn, n=20):
        self.user_dict = user_dict
        self.n = n
        self.words = np.array([], dtype=np.int64)
        self.knn = knn
        self.myknn = KNeighborsClassifier(n)

    def get_closest_to_single_word(self):
        for word in self.user_dict:
            _, neighbors_ind = self.knn.kneighbors(get_embedding([word]).detach().numpy())
            self.words = np.append(self.words, neighbors_ind)

    def get_dict_embedding(self):
        ans = np.array([[0.0] * dim])
        for i in self.user_dict:
            ans += self.get_embedding([i]).detach().numpy()[0]
        return ans / len(self.user_dict)

    def fit(self, n=10):
        word_emb = base_embeddings[np.unique(self.words)]
        self.myknn.fit(word_emb, [0] * len(word_emb))

    def get_closest_to_dict(self, n=20):
        self.get_closest_to_single_word()
        dict_emb = self.get_dict_embedding()
        self.fit(n)
        _, neighbors_ind = self.myknn.kneighbors(dict_emb)
        real_ids = self.words[neighbors_ind[0]]
        return real_ids

    def get_embedding(self, tokens):
        token_ids = torch.tensor(tokenizer.convert_tokens_to_ids(tokens))
        outputs = bert_embedder(token_ids.unsqueeze(0))
        last_hidden_states = outputs.last_hidden_state
        return last_hidden_states[0]


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


def prepare_bert_tokenizer_and_embedder(bert_model_name):
    tokenizer = BertTokenizer.from_pretrained(bert_model_name)
    bert_embedder = BertModel.from_pretrained(bert_model_name)
    bert_embedder.pooler = nn.Identity()
    del bert_embedder.encoder.layer[:]

    return tokenizer, bert_embedder


tokenizer, bert_embedder = prepare_bert_tokenizer_and_embedder("google-bert/bert-base-cased")


def get_embedding(tokens):
    token_ids = torch.tensor(tokenizer.convert_tokens_to_ids(tokens))
    outputs = bert_embedder(token_ids.unsqueeze(0))
    last_hidden_states = outputs.last_hidden_state

    return last_hidden_states[0]


base_embeddings = np.array([[0] * 768])
for i in range(0, len(base_txt)):
    base_embeddings = np.concatenate((base_embeddings, get_embedding([base_txt[i]]).detach().numpy()))
base_embeddings = base_embeddings[1:]
knn = KNeighborsClassifier(20)
knn.fit(base_embeddings, [0]*base_embeddings.shape[0])


@check_login
def index(request):
    global Base, UserWord, base_txt, base_ger_txt, base_eng_txt
    if request.session["lang"] and request.session["lang"] == "ger" and base_txt != base_ger_txt:
        Base = BaseGerm
        UserWord = UserWordGerm
        if base_ger_txt == "":
            base_ger_txt = list(map(lambda x: x.word_eng, BaseGerm.objects.all()))
        base_txt = base_ger_txt
    elif request.session["lang"] and request.session["lang"] == "eng" and base_txt != base_eng_txt:
        Base = BaseEng
        UserWord = UserWordEng
        base_txt = base_eng_txt
    user_dict = list(map(lambda x: Base.objects.filter(id=x.word_id_id).first().word_eng,
                         UserWord.objects.filter(user_id_id=request.session["id"])[:10]))
    myknn = myKNN(user_dict, knn, 20)
    ind = myknn.get_closest_to_dict()
    words = []
    idxs = []
    for i in ind:
        word = Base.objects.all()[int(i)]
        idxs.append(word.id)
        words.append(word.word_eng + " - " + word.word_rus)
    content = {"words": words, "idxs": idxs}
    return render(request, "similar_words/index.html", content)


def get_recommended_words(request):
    global Base, UserWord, base_txt, base_ger_txt, base_eng_txt
    if request.session["lang"] and request.session["lang"] == "ger" and base_txt != base_ger_txt:
        Base = BaseGerm
        UserWord = UserWordGerm
        if base_ger_txt == "":
            base_ger_txt = list(map(lambda x: x.word_eng, BaseGerm.objects.all()))
        base_txt = base_ger_txt
    elif request.session["lang"] and request.session["lang"] == "eng" and base_txt != base_eng_txt:
        Base = BaseEng
        UserWord = UserWordEng
        base_txt = base_eng_txt
    word_amount = len(UserWord.objects.filter(user_id_id=request.session["id"]))
    user_dict = list(map(lambda x: Base.objects.filter(id=x.word_id_id).first().word_eng,
                         UserWord.objects.filter(user_id_id=request.session["id"])[max(word_amount-10, 0):]))

    amount = request.GET.get('amount', 5)
    myknn = myKNN(user_dict, knn, int(amount))
    ind = myknn.get_closest_to_dict()
    words = []
    idxs = []
    for i in ind:
        word = Base.objects.all()[int(i)]
        idxs.append(word.id)
        words.append(word.word_eng + " - " + word.word_rus)
    content = {"words": words, "ids": idxs}
    return JsonResponse(content)
