# -*- coding: utf-8 -*-
# Core Django Imports
from django.urls import path

# Monta Core Imports
from monta_authentication import views

urlpatterns = [
    path("login/", views.monta_authenticate_user, name="monta_login"),
    path("logout/", views.monta_logout_user, name="monta_logout"),
]

