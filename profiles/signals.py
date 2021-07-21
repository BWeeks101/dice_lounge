from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
# ...................................................Modified Boutique-Ado Code
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
        Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()

# ...............................................End Modified Boutique-Ado Code


@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    email_address.set_as_primary()
    EmailAddress.objects.filter(
        user=email_address.user).exclude(primary=True).delete()
