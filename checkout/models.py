# ...................................................Modified Boutique-Ado Code
import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from profiles.models import UserProfile


# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    first_name = models.CharField(max_length=25, null=False, blank=False)
    last_name = models.CharField(max_length=25, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(
        blank_label='Country *',
        null=False,
        blank=False,
        default=settings.DEFAULT_COUNTRY
    )
    delivery_first_name = models.CharField(
        max_length=25, null=False, blank=False)
    delivery_last_name = models.CharField(
        max_length=25, null=False, blank=False)
    delivery_address1 = models.CharField(
        max_length=80, null=False, blank=False)
    delivery_address2 = models.CharField(max_length=80, null=True, blank=True)
    delivery_town_or_city = models.CharField(
        max_length=40, null=False, blank=False)
    delivery_county = models.CharField(max_length=80, null=True, blank=True)
    delivery_postcode = models.CharField(
        max_length=20, null=False, blank=False)
    delivery_country = CountryField(
        blank_label='Country *',
        null=False,
        blank=False,
        default=settings.DEFAULT_COUNTRY
    )
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
            Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
            update grand total each time a line item is added, accounting for
            delivery costs.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            )
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
            Override the original save method to set the order number if it
            hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product_id = models.IntegerField(
        null=True, blank=False, default=-1)
    product = models.CharField(
        max_length=254, blank=False, null=False)
    sub_product_line = models.CharField(
        max_length=254, blank=False, null=False)
    product_line = models.CharField(
        max_length=254, blank=False, null=False)
    quantity = models.IntegerField(
        null=False, blank=False, default=0)
    item_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        default=0.00
    )
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        default=0.00
    )

    def save(self, *args, **kwargs):
        """
            Override the original save method to set the lineitem total.
        """
        self.lineitem_total = self.item_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'ID {self.product_id} on order {self.order.order_number}'
# ...............................................End Modified Boutique-Ado Code
