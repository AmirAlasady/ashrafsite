from django.urls import path

from . import views

app_name = "academy"

urlpatterns = [
    path("", views.academy_list, name="list"),
    path("<int:pk>/", views.academy_detail, name="detail"),
]
