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
     path(
          'detail/<int:product_id>/',
          views.product_detail,
          name='product_detail'
     ),
     path(
          'get_lookup/<lookup_type>/',
          views.get_lookup,
          name='get_lookup'
     ),
     path(
          'product_management/',
          views.product_management,
          name='product_management'),
     path(
          'add/<request_config_key>/',
          views.add,
          name='add'
     ),
     path(
          'edit/<request_config_key>/<int:object_id>/',
          views.edit,
          name='edit'
     )
]
