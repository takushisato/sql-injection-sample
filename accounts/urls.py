from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("bad-login/", views.bad_login, name="bad_login"),
]
