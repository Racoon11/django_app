from django.db import models
from django.contrib.auth.models import User

class Information(models.Model):
    id = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    level = models.CharField(max_length=20)
    words = models.IntegerField(default=0)
    def __str__(self):
        return User.objects.filter(id=self.id)[0].username
