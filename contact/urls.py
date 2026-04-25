from django.urls import path

from . import views

app_name = "contact"

urlpatterns = [
    path("", views.contact_view, name="form"),
    path("thanks/", views.contact_success, name="success"),
]
