from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("behind-the-scenes/", views.bts_gallery, name="bts_gallery"),
    path("casting/", views.casting, name="casting"),
]
