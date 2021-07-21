# ...................................................Modified Boutique-Ado Code
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
     path('', views.checkout, name='checkout'),
     path('validate_postcode/',
          views.validate_postcode, name='validate_postcode'),
     path('validate_country/',
          views.validate_country, name='validate_country'),
     path('checkout_success/<order_number>',
          views.checkout_success, name='checkout_success'),
     path('cache_checkout_data/',
          views.cache_checkout_data, name='cache_checkout_data'),
     path('wh/', webhook, name='webhook')
]
# ...............................................End Modified Boutique-Ado Code
