from django.shortcuts import render, redirect, reverse
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from products.views import get_search_request, is_product_hidden
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
                f'Unable to allocate stock.  Product ({product_id}) not \
                    found.',
                'from__checkout_basket'
            )
            unable_to_allocate = True
            break

        # If the product is hidden, send a message and break
        if is_product_hidden(product) is True:
            messages.error(
                request,
                f'Unable to allocate stock.  Unfortunately, {product.name} is \
                    no longer available.',
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
    # If no postcode provided, return no_postcode_provided
    if postcode is None or len(postcode) == 0:
        return 'no_postcode_provided'

    # Submit the postcode to postcodes.io
    response = requests.get(
        f'https://api.postcodes.io/postcodes/{postcode}/validate')

    # If the response status code is 200 (successful response, not necessarily
    # successful postcode validation), return the result in json format
    if response.status_code == 200:
        return response.json()['result']

    # Otherwise return failed
    return 'failed'


# POST request to validate postcode
@require_POST
def validate_postcode(request):
    # submit the postcode to postcodes.io, and return the response in json
    # format
    return JsonResponse(
        {
            'result': submit_postcode(request.POST.get('postcode'))
        }
    )


# get country code and name as a formatted object
# By default, will use the settings.DEFAULT_COUNTRY value as the country code
def get_country(country_code=settings.DEFAULT_COUNTRY):
    # If a country code is provided but is not valid, use the value from
    # settings.DEFAULT_COUNTRY
    if (country_code is None or country_code == '' or
            country_code not in dict(countries)):
        country_code = settings.DEFAULT_COUNTRY

    # Define a country object, with the country code as 'code' and the country
    # name as 'name'
    country = {
        'code': country_code,
        'name': dict(countries)[country_code]
    }

    # return the country object
    return country


# get list of valid country names
# iterate over the settings.COUNTRIES_ONLY list, and return a list of country
# objects (formatted by get_country()), sorted by code.
# Optionally, if sort_by_name is set to True, the results will be sorted by
# name.
def get_countries_only(sort_by_name=False):
    # define empty list
    countries = []

    # iterate over settings.COUNTRIES_ONLY values, calling get_country() for
    # each, and appending the returned object to the countries list
    for country in settings.COUNTRIES_ONLY:
        countries.append(get_country(country))

    # define the sort by code function
    def sort_code(e):
        return e['code']

    # define the sort by name function
    def sort_name(e):
        return e['name']

    # if sort by name is true, sort by name.  Otherwise sort by code (default)
    if sort_by_name is True:
        countries.sort(key=sort_name)
    else:
        countries.sort(key=sort_code)

    # Return the list
    return countries


# POST request to validate country
@require_POST
def validate_country(request):
    # Get the country code from the POST request
    country_code = request.POST.get('country_code')

    # If the code is not present in settings.COUNTRIES_ONLY...
    if country_code not in settings.COUNTRIES_ONLY:
        # return a json formatted object containing false, and a list of
        # valid countries
        return JsonResponse({
            'result': False,
            'valid_countries': get_countries_only(sort_by_name=True)
        })

    # Otherwise return true formatted in a json object for consistency with a
    # false result, and the results from postcodes.io
    return JsonResponse({'result': True})


# ...................................................Modified Boutique-Ado Code
def checkout(request):
    """
        Display the checkout and handle payment submission
    """
    # Redirect search requests
    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    # Check the basket for errors and if found, send a message, deallocate any
    # allocated stock, then redirect the user to the basket
    basket_errors = request.session.get('basket_errors', 0)
    if basket_errors > 0:
        messages.error(
            request,
            "Please resolve errors with your basket before proceeding",
            'from__checkout_basket'
        )
        deallocate_stock(request)
        return redirect(reverse('view_basket'))

    # Get stripe keys
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Get the basket object from session
    basket = request.session.get('basket', {})

    # POST Request.  Attempt to process the order
    if request.method == 'POST':
        # Define the form_data object from POST data, setting the delivery
        # details to the billing address by default
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

        # If the 'use billing address' for delivery option was not selected,
        # update the delivery details in the form_data
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

        # If either the billing or delivery postcodes fail to validate, send
        # a message, deallocate stock, and return the user to the checkout
        if (submit_postcode(form_data['postcode']) is not True or
                submit_postcode(form_data['delivery_postcode']) is not True):
            messages.error(
                request,
                'Please provide a valid UK postcode for billing and delivery.',
                'from__checkout_basket'
            )
            deallocate_stock(request)
            return redirect(reverse('checkout'))

        # If either the billing or delivery countries fail to validate, send a
        # message, deallocate stock, and return the user to the checkout
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

        # use the form_data to populate an instance of OrderForm
        order_form = OrderForm(form_data)
        # If the form is valid...
        if order_form.is_valid():
            # create an order object by saving the OrderForm instance
            order = order_form.save(commit=False)
            # get the strip pid and add it to the order object along with the
            # the basket contents in json format, then save the order
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()
            # Iterate over the basket, and for each item...
            for product_id, quantity in basket.items():
                try:
                    # Get the product from the Products table
                    product_obj = Product.objects.get(id=product_id)
                    if is_product_hidden(product_obj) is True:
                        raise Exception
                # If the product does not exist, send a message, delete the
                # order, deallocate stock and return the user to the basket
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
                # If the product is hidden, send a message, delete the order,
                # deallocate stock and return the user to the basket
                except Exception:
                    messages.error(
                        request,
                        "Unfortunately, one of the products in your basket is \
                            no longer available for purchase.",
                        'from__checkout_basket'
                    )
                    order.delete()
                    deallocate_stock(request)
                    return redirect(reverse('view_basket'))
                else:
                    # Get the product name
                    product = product_obj.name
                    # Get the sub_product_line name
                    sub_product_line = product_obj.sub_product_line.name
                    # Get the product_line name
                    product_line = (
                        product_obj.sub_product_line.product_line.name)
                    # Get the price, corrected for any offers
                    item_price = product_obj.get_price()['price']
                    # Create an order line item instance using these details
                    # plus the quantity of the item in the basket
                    order_line_item = OrderLineItem(
                        order=order,
                        product_id=product_id,
                        product=product,
                        sub_product_line=sub_product_line,
                        product_line=product_line,
                        item_price=item_price,
                        quantity=quantity,
                    )
                    # save the order line item (which will update the basket
                    # total via signal)
                    order_line_item.save()

            # Write the value of the 'save info' check box to the session
            request.session['save_info'] = 'save-info' in request.POST
            # Redirect the user to checkout success
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))
        # The form is invalid, so send a message, deallocate stock and return
        # the user to the checkout
        else:
            messages.error(
                request,
                'There was an error with your form.  Please double check your \
                information.',
                'from__checkout_basket'
            )
            deallocate_stock(request)
            return redirect(reverse('checkout'))
    # GET Request
    else:
        # If the basket is empty, send a message and redirect the user to
        # all_games
        if not basket:
            messages.error(
                request,
                "There's nothing in your basket at the moment.",
                'from__checkout_basket'
            )
            return redirect(reverse('all_games'))

        # Run the basket_contents context processor and get the basket object
        # from the results
        current_basket = basket_contents(request)['basket']

        # Create stripe data
        stripe_total = round(current_basket['grand_total'] * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Get a country object for the default country
        selected_country = get_country(settings.DEFAULT_COUNTRY)

        # If the user is logged in...
        if request.user.is_authenticated:
            # Get the user profile
            try:
                profile = UserProfile.objects.get(user=request.user)
            # User profile doesn't exist, so set order_form to an empty
            # instance of OrderForm
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
            # Otherwise we have the profile, so set order_form to an instance
            # of OrderForm with initial data from the user profile
            else:
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

                # get a country object for the country in the user profile
                selected_country = get_country(profile.default_country)
        # User is not logged in, so set order_form to an empty instance of
        # order_form
        else:
            order_form = OrderForm()

        # If the stripe public key is missing, send a warning message - this
        # Should never occur in prod!
        if not stripe_public_key:
            messages.warning(
                request,
                'Stripe public key is missing.  \
                Did you forget to set it in your environment?'
            )

        # Define the context object, including the name of the view, the
        # order form, selected country and stripe keys
        context = {
            'view': 'checkout',
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'selected_country': selected_country
        }

        # Render the checkout view, passing the context
        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
        Handle successful checkouts
    """
    # Redirect search requests
    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    # Get the users 'save info' selection from the session
    save_info = request.session.get('save_info')

    # Get the order object
    try:
        order = Order.objects.get(order_number=order_number)
    # If the order does not exist, set order to None and send a message
    except Order.DoesNotExist:
        order = None
        messages.error(
            request,
            f'Unable to locate order with order number:\n{order_number}\n \
            Please contact us for assistance ASAP.',
            'from__checkout_success_basket'
        )
    # If we got the order...
    if order is not None:
        # If the user is logged in...
        if request.user.is_authenticated:
            # Get the users profile
            try:
                profile = UserProfile.objects.get(user=request.user)
            # If the profile does not exist, pass
            except UserProfile.DoesNotExist:
                pass
            # otherwise we got the profile...
            else:
                # Attach the user's profile to the order and save it
                order.user_profile = profile
                order.save()

                # If save_info is true, update the users profile data with the
                # details from the order
                if save_info:
                    # Create a profile data object from the order address
                    # details
                    profile_data = {
                        'default_phone_number': order.phone_number,
                        'default_street_address1': order.street_address1,
                        'default_street_address2': order.street_address2,
                        'default_town_or_city': order.town_or_city,
                        'default_county': order.county,
                        'default_postcode': order.postcode,
                        'default_country': order.country
                    }
                    # Create an instance of the UserProfileForm using the
                    # profile_data object
                    user_profile_form = UserProfileForm(
                        profile_data,
                        instance=profile
                    )
                    # If the form is valid, save it
                    if user_profile_form.is_valid():
                        user_profile_form.save()
                    # Create a user data object from the order name details
                    user_data = {
                        'first_name': order.first_name,
                        'last_name': order.last_name
                    }
                    # Create an instance of the UserForm using the user data
                    # object
                    user_form = UserForm(
                        user_data,
                        instance=profile.user
                    )
                    # If the form is valid, save it
                    if user_form.is_valid():
                        user_form.save()

        # Send a message to let the user know that the order was processed
        messages.success(
            request,
            f'Order successfully processed! Your order number is: \
            \n{order_number}\nA confirmation email will be sent to: \
            \n{order.email}',
            'from__checkout_success_basket'
        )

        # If the basket still exists within session, remove it
        if 'basket' in request.session:
            del request.session['basket']

        # Define a context object with the view, order object and delivery
        # country name
        context = {
            'view': 'checkout_success',
            'order': order,
            'country_name': get_country(order.delivery_country)['name']
        }

        # render the order details page, passing the context
        return render(request, 'checkout/order_details.html', context)

    # No order, so redirect the user to the basket
    return redirect(reverse('view_basket'))

# ...............................................End Modified Boutique-Ado Code
