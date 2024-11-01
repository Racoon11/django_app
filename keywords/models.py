from django.db import models

# Create your models here.


class CheckWordsEng(models.Model):
    word_eng = models.CharField(max_length=50)
    word_rus = models.CharField(max_length=50, default="none")


class CheckWordsGer(models.Model):
    word_eng = models.CharField(max_length=50)
    word_rus = models.CharField(max_length=50, default="none")
