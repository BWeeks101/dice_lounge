"""
dice_lounge URL Configuration
Products app
"""
from django.urls import path
from . import views

urlpatterns = [
     path('', views.all_games, name='all_games'),
     path('search_results/', views.search_results, name='search_results'),
     path(
          '<int:product_line_id>/',
          views.products,
          name='products'
     ),
]
