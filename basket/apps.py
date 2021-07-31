from django.apps import AppConfig


# Django admin config for the Basket model
class BasketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basket'
