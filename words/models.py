from django.db import models
from django.contrib.auth.models import User
from users.models import Information
import datetime
from django.utils import timezone
from random import randint


deltas = [1, 3, 7, 30, 120]
deltas = list(map(lambda x: datetime.timedelta(days=x), deltas))
n = 8050

class BaseEng(models.Model):
    word_eng = models.CharField(max_length=50)
    word_rus = models.CharField(max_length=60)
    def __str__(self):
        return self.word_eng

class UserWordEng(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    word_id = models.ForeignKey(BaseEng, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    when_to_train = models.DateTimeField(default=timezone.now)

    def is_to_train(self):
        now = timezone.now()
        return now >= self.when_to_train
    def is_learnt(self):
        return self.count >= 5
    def train(self, correct):

        if correct:
            self.when_to_train = timezone.now() + deltas[self.count]
            self.count += 1
        else:
            self.when_to_train = timezone.now() + deltas[0]


class BaseGerm(models.Model):
    word_eng = models.CharField(max_length=50)
    word_rus = models.CharField(max_length=60)
    def __str__(self):
        return self.word_eng


class UserWordGerm(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    word_id = models.ForeignKey(BaseGerm, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    when_to_train = models.DateTimeField(default=timezone.now)

    def is_to_train(self):
        now = timezone.now()
        return now >= self.when_to_train
    def is_learnt(self):
        return self.count >= 5
    def train(self, correct):

        if correct:
            self.when_to_train = timezone.now() + deltas[self.count]
            self.count += 1
        else:
            self.when_to_train = timezone.now() + deltas[0]



