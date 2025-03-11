from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path('', views.index, name='index'),
    path("get_answer", views.get_answer)
    ]
