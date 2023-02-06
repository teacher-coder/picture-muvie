from . import views

from django.urls import path

urlpatterns = [
    path("", views.lyrics_post, name="lyrics_post")
]
