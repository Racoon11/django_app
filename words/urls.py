from django.urls import path

from . import views

app_name = "words"

urlpatterns = [
    path('', views.index, name='index'),
    path('train', views.train, name='train'),
    path('mywords', views.mywords, name='mywords'),
    path("add", views.add, name="add"),
    path('mywords/fetch', views.fetch, name='fetch'),
    path("train/finish", views.finish, name="finish"),
    path("language", views.change_language, name="language"),
    path("amount", views.get_amount_to_train, name='amount'),
]
