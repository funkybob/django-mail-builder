from django.urls import path

from . import views

urlpatterns = [
    path("", views.SimpleView.as_view()),
]
