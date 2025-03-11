from django.urls import path

from . import views

app_name = "similar_words"

urlpatterns = [
    path('', views.index, name='index'),
    path('five', views.get_recommended_words, name='five')
    ]
