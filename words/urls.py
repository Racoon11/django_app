from django.urls import path

from . import views

app_name = "words"

urlpatterns = [
    path('', views.index, name='index'),
    path('train', views.train, name='train'),
    path('mywords', views.mywords, name='mywords'),
]
