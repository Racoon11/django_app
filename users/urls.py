from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("registration", views.registration, name='registration'),
    path("login", views.login, name='login'),
    path('email_exists', views.email_exists, name='email_exists'),
    path('', views.index, name='index'),
]
