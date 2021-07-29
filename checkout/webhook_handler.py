# ...................................................Modified Boutique-Ado Code
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
import json
import time


class StripeWH_Handler:
    """
        Handle Stripe webhooks
    """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
            Send the user a confirmation email
        """
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """
            Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
            Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info
        billing_first_name = intent.metadata.billing_first_name
        billing_last_name = intent.metadata.billing_last_name
        billing_details = intent.charges.data[0].billing_details
        delivery_first_name = intent.metadata.delivery_first_name
        delivery_last_name = intent.metadata.delivery_last_name
        delivery_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the delivery details
        for field, value in delivery_details.address.items():
            if value == "":
                delivery_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.user.first_name = billing_first_name
                profile.user.last_name = billing_last_name
                profile.default_phone_number = billing_details.phone
                profile.default_street_address1 = (
                    billing_details.address.line1)
                profile.default_street_address2 = (
                    billing_details.address.line2)
                profile.default_town_or_city = billing_details.address.city
                profile.default_county = billing_details.address.state
                profile.default_postcode = billing_details.address.postal_code
                profile.default_country = billing_details.address.country
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    first_name__iexact=billing_first_name,
                    last_name__iexact=billing_last_name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    town_or_city__iexact=billing_details.address.city,
                    county__iexact=billing_details.address.state,
                    postcode__iexact=billing_details.address.postal_code,
                    country__iexact=billing_details.address.country,
                    delivery_first_name__iexact=delivery_first_name,
                    delivery_last_name__iexact=delivery_last_name,
                    delivery_address1__iexact=delivery_details.address.line1,
                    delivery_address2__iexact=delivery_details.address.line2,
                    delivery_town_or_city__iexact=(
                        delivery_details.address.city),
                    delivery_county__iexact=delivery_details.address.state,
                    delivery_postcode__iexact=(
                        delivery_details.address.postal_code),
                    delivery_country__iexact=delivery_details.address.country,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_confirmation_email(order)
            success_msg = 'SUCCESS: Verified order already in database'
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | {success_msg}',
                status=200
            )
        else:
            order = None
            try:
                order = Order.objects.create(
                    user_profile=profile,
                    first_name=billing_first_name,
                    last_name=billing_last_name,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    town_or_city=billing_details.address.city,
                    county=billing_details.address.state,
                    postcode=billing_details.address.postal_code,
                    country=billing_details.address.country,
                    delivery_first_name=delivery_first_name,
                    delivery_last_name=delivery_last_name,
                    delivery_address1=delivery_details.address.line1,
                    delivery_address2=delivery_details.address.line2,
                    delivery_town_or_city=(
                        delivery_details.address.city),
                    delivery_county=delivery_details.address.state,
                    delivery_postcode=(
                        delivery_details.address.postal_code),
                    delivery_country=delivery_details.address.country,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                for product_id, quantity in json.loads(basket).items():
                    product_obj = Product.objects.get(id=product_id)
                    product = product_obj.name
                    sub_product_line = product_obj.sub_product_line.name
                    product_line = (
                        product_obj.sub_product_line.product_line.name)
                    item_price = product_obj.get_price()['price']
                    order_line_item = OrderLineItem(
                        order=order,
                        product_id=product_id,
                        product=product,
                        sub_product_line=sub_product_line,
                        product_line=product_line,
                        quantity=quantity,
                        item_price=item_price
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500
                )

        self._send_confirmation_email(order)
        wh_success_msg = 'SUCCESS: Created order in webhook'
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | {wh_success_msg}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
            Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
# ...............................................End Modified Boutique-Ado Code
