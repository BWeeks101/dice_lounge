"""
dice_lounge URL Configuration
Home app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
]
