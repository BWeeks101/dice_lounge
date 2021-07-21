# ...................................................Modified Boutique-Ado Code
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from allauth.account.models import EmailAddress


class UserProfile(models.Model):
    """
        A user profile model for maintaining default delivery information and
        order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True)
    default_county = models.CharField(
        max_length=80, null=True, blank=True)
    default_postcode = models.CharField(
        max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country', null=True, blank=True)

    def __str__(self):
        return self.user.username

# ...............................................End Modified Boutique-Ado Code

    def add_email_address(self, request, new_email):
        return EmailAddress.objects.add_email(
            request, self.user, new_email, confirm=True)
