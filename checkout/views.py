from django.shortcuts import render, redirect, reverse
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from products.views import get_search_request
from basket.context_processors import basket_contents
from profiles.forms import UserProfileForm, UserForm
from profiles.models import UserProfile
import stripe
import json
import requests
from django_countries import countries


# Create your views here.
# Deallocate stock for a basket
def deallocate_stock(request):
    # Get the allocated stock object
    stock_allocated = request.session.get('stock_allocated')

    # If there is no allocated stock object, return
    if stock_allocated is None:
        return

    # Iterate over the allocated stock object
    for product_id in stock_allocated:
        # Get the product
        product = Product.objects.get(pk=product_id)
        # If stock was allocated for this product...
        if stock_allocated[product_id]['allocated'] is True:
            # Restore the stock
            product.stock += stock_allocated[product_id]['quantity']
            # Save the product
            product.save()
            # Set allocated to false in case the loop is unable to complete for
            # any reason, and is subsequently executed again
            stock_allocated[product_id]['allocated'] = False

    # When the loop completes, remove the allocated stock object from session
    request.session.pop('stock_allocated')


# Allocate stock for a basket
def allocate_stock(request):
    # Get the basket
    basket = request.session.get('basket')

    # If the basket does not exist, or is empty, return false
    if basket is None or len(basket) == 0:
        messages.error(
            request,
            'Your basket does not contain any items.',
            'from__checkout_basket'
        )
        return False

    # Create the local basket dict.  Change the value of each object from
    # the quantity, to a dict containing the quantity, and whether the stock
    # is allocated
    local_basket = {}
    for product_id in basket:
        local_basket[product_id] = {
            'quantity': basket[product_id],
            'allocated': False
        }

    # Boolean to determine if the basket contains any objects where we couldn't
    # allocate stock
    unable_to_allocate = False

    # Iterate over the local basket, and attempt to allocate stock
    for product_id in local_basket:
        # Try to return the product from the Product model, and if it doesn't
        # exist, send a message and break
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            product = None
            messages.error(
                request,
                f'Unable to allocate stock.  \
                Product ({product_id}) not found.',
                'from__checkout_basket'
            )
            unable_to_allocate = True
            break

        # Got the product, so if the stock is >= quantity, reduce the stock
        # by the quantity
        if product.stock >= local_basket[product_id]['quantity']:
            product.stock -= local_basket[product_id]['quantity']
            product.save()
        else:
            # Stock < quantity, so send a message and break
            msg = f'Insufficient stock of {product.name} to fullfill order. \
                Please revise your basket.'
            if product.stock == 0:
                msg = f'{product.name} is currently out of stock.  Please \
                revise your basket.'
            messages.error(request, msg, 'from__checkout_basket')
            unable_to_allocate = True
            break

    # Add the local basket to the session
    request.session['stock_allocated'] = local_basket

    # If unable_to_allocate is true we ran into an error, so deallocate any
    # allocated stock and return false
    if unable_to_allocate is True:
        deallocate_stock(request)
        return False

    # Otherwise all stock was allocated, so return true
    return True


# ...................................................Modified Boutique-Ado Code
@require_POST
def cache_checkout_data(request):
    stock_allocated = allocate_stock(request)
    try:
        if stock_allocated is False:
            raise Exception
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user
        })
        return HttpResponse(status=200)
    except Exception as e:
        if stock_allocated is True:
            deallocate_stock(request)
            messages.error(
                request,
                'Sorry, your payment cannot be processed right now.  Please \
                try again later.',
                'from__checkout_basket'
            )
        return HttpResponse(content=e, status=400)
# ...............................................End Modified Boutique-Ado Code


# validate postcode using postcodes.io
def submit_postcode(postcode):
    if postcode is None or len(postcode) == 0:
        return 'no_postcode_provided'
    response = requests.get(
        f'https://api.postcodes.io/postcodes/{postcode}/validate')

    if response.status_code == 200:
        return response.json()['result']

    return 'failed'


# POST request to validate postcode
@require_POST
def validate_postcode(request):
    return JsonResponse(
        {
            'result': submit_postcode(request.POST.get('postcode'))
        }
    )


# get country code and name as a formatted object
def get_country(country_code=settings.DEFAULT_COUNTRY):
    if (country_code is None or country_code == '' or
            country_code not in dict(countries)):
        country_code = settings.DEFAULT_COUNTRY
    country = {
        'code': country_code,
        'name': dict(countries)[country_code]
    }

    return country


# get list of valid country names
def get_countries_only(sort_by_name=False):
    countries = []
    for country in settings.COUNTRIES_ONLY:
        countries.append(get_country(country))

    def sort_code(e):
        return e['code']

    def sort_name(e):
        return e['name']

    if sort_by_name is True:
        countries.sort(key=sort_name)
    else:
        countries.sort(key=sort_code)

    return countries


# validate country
@require_POST
def validate_country(request):
    country_code = request.POST.get('country_code')
    if country_code not in settings.COUNTRIES_ONLY:
        return JsonResponse({
            'result': False,
            'valid_countries': get_countries_only(sort_by_name=True)
        })

    return JsonResponse({'result': True})


# ...................................................Modified Boutique-Ado Code
def checkout(request):
    """
        Display the checkout and handle payment submission
    """
    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    basket_errors = request.session.get('basket_errors', 0)
    if basket_errors > 0:
        messages.error(
            request,
            "Please resolve errors with your basket before proceeding",
            'from__checkout_basket'
        )
        deallocate_stock(request)
        return redirect(reverse('view_basket'))

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})

        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
            'delivery_first_name': request.POST['first_name'],
            'delivery_last_name': request.POST['last_name'],
            'delivery_address1': request.POST['street_address1'],
            'delivery_address2': request.POST['street_address2'],
            'delivery_town_or_city': request.POST['town_or_city'],
            'delivery_county': request.POST['county'],
            'delivery_postcode': request.POST['postcode'],
            'delivery_country': request.POST['country'],
        }

        if request.POST.get('use-billing-address') != 'on':
            form_data['delivery_first_name'] = (
                request.POST['delivery_first_name'])
            form_data['delivery_last_name'] = (
                request.POST['delivery_last_name'])
            form_data['delivery_address1'] = request.POST['delivery_address1']
            form_data['delivery_address2'] = request.POST['delivery_address2']
            form_data['delivery_town_or_city'] = (
                request.POST['delivery_town_or_city'])
            form_data['delivery_county'] = request.POST['delivery_county']
            form_data['delivery_postcode'] = request.POST['delivery_postcode']
            form_data['delivery_country'] = request.POST['delivery_country']

        if (submit_postcode(form_data['postcode']) is not True or
                submit_postcode(form_data['delivery_postcode']) is not True):
            messages.error(
                request,
                'Please provide a valid UK postcode for billing and delivery.',
                'from__checkout_basket'
            )
            deallocate_stock(request)
            return redirect(reverse('checkout'))

        if (form_data['country'] not in settings.COUNTRIES_ONLY or
                form_data['delivery_country'] not in settings.COUNTRIES_ONLY):
            messages.error(
                request,
                'Your selected country is not on our list of approved \
                shipping destinations.',
                'from__checkout_basket'
            )
            deallocate_stock(request)
            return redirect(reverse('checkout'))

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()
            for product_id, quantity in basket.items():
                try:
                    product_obj = Product.objects.get(id=product_id)
                    product = product_obj.name
                    sub_product_line = product_obj.sub_product_line.name
                    product_line = (
                        product_obj.sub_product_line.product_line.name)
                    item_price = product_obj.price
                    order_line_item = OrderLineItem(
                        order=order,
                        product_id=product_id,
                        product=product,
                        sub_product_line=sub_product_line,
                        product_line=product_line,
                        item_price=item_price,
                        quantity=quantity,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "One of the products in your basket wasn't found in \
                            our database.  Please call us for assistance!",
                        'from__checkout_basket'
                    )
                    order.delete()
                    deallocate_stock(request)
                    return redirect(reverse('view_basket'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))
        else:
            messages.error(
                request,
                'There was an error with your form.  Please double check your \
                information.',
                'from__checkout_basket'
            )
            deallocate_stock(request)
            return redirect(reverse('checkout'))
    else:
        # GET Request
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(
                request,
                "There's nothing in your basket at the moment.",
                'from__checkout_basket'
            )
            return redirect(reverse('all_games'))

        current_basket = basket_contents(request)['basket']
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        selected_country = get_country(settings.DEFAULT_COUNTRY)

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'first_name': profile.user.first_name,
                    'last_name': profile.user.last_name,
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town_or_city': profile.default_town_or_city,
                    'county': profile.default_county,
                    'postcode': profile.default_postcode,
                    'country': profile.default_country,
                    'delivery_first_name': profile.user.first_name,
                    'delivery_last_name': profile.user.last_name,
                    'delivery_address1': profile.default_street_address1,
                    'delivery_address2': profile.default_street_address2,
                    'delivery_town_or_city': profile.default_town_or_city,
                    'delivery_county': profile.default_county,
                    'delivery_postcode': profile.default_postcode,
                    'delivery_country': profile.default_country,
                })

                selected_country = get_country(profile.default_country)
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(
                request,
                'Stripe public key is missing.  \
                Did you forget to set it in your environment?'
            )

        context = {
            'view': 'checkout',
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'selected_country': selected_country
        }

        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
        Handle successful checkouts
    """
    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    save_info = request.session.get('save_info')
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        order = None
        messages.error(
            request,
            f'Unable to locate order with order number:\n{order_number}\n \
            Please contact us for assistance ASAP.',
            'from__checkout_success_basket'
        )
    if order is not None:
        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            # Attach the user's profile to the order
            order.user_profile = profile
            order.save()

            # save the user's info
            if save_info:
                profile_data = {
                    'default_phone_number': order.phone_number,
                    'default_country': order.country,
                    'default_postcode': order.postcode,
                    'default_town_or_city': order.town_or_city,
                    'default_street_address1': order.street_address1,
                    'default_street_address2': order.street_address2,
                    'default_county': order.county,
                }
                user_profile_form = UserProfileForm(
                    profile_data,
                    instance=profile
                )
                if user_profile_form.is_valid():
                    user_profile_form.save()
                user_data = {
                    'first_name': order.first_name,
                    'last_name': order.last_name
                }
                user_form = UserForm(
                    user_data,
                    instance=profile.user
                )
                if user_form.is_valid():
                    user_form.save()

        messages.success(
            request,
            f'Order successfully processed! Your order number is: \
            \n{order_number}\nA confirmation email will be sent to: \
            \n{order.email}',
            'from__checkout_success_basket'
        )

        if 'basket' in request.session:
            del request.session['basket']

        context = {
            'view': 'checkout_success',
            'order': order,
            'country_name': get_country(order.delivery_country)['name']
        }

        return render(request, 'checkout/order_details.html', context)

    return redirect(reverse('view_basket'))

# ...............................................End Modified Boutique-Ado Code
