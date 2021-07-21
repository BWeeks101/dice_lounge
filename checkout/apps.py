from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    # ........................................................Boutique-Ado Code
    def ready(self):
        import checkout.signals
    # ....................................................End Boutique-Ado Code
