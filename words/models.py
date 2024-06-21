from django.db import models
from django.contrib.auth.models import User
from users.models import Information
import datetime
from django.utils import timezone


deltas = [1, 3, 7, 30, 120]
deltas = list(map(lambda x: datetime.timedelta(days=x), deltas))

class Base(models.Model):
    word_eng = models.CharField(max_length=50)
    word_rus = models.CharField(max_length=60)
    def __str__(self):
        return self.word_eng
class UserWord(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    word_id = models.ForeignKey(Base, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    when_to_train = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return Base.objects.filter(id=self.word_id)[0].word_eng
    def is_to_train(self):
        now = timezone.now()
        return now >= self.when_to_train
    def is_learnt(self):
        return self.count >= 5
    def train_correct(self):
        self.when_to_train = timezone.now() + deltas[self.count]


