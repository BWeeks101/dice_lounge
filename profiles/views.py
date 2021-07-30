# ...................................................Modified Boutique-Ado Code
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import UserProfile
from .forms import UserProfileForm, UserForm
from products.views import get_search_request
from checkout.models import Order
from checkout.views import get_country
from allauth.account.models import EmailAddress


# Create your views here.
@login_required
def profile(request):
    """
        Display the user's profile.
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    profile = get_object_or_404(UserProfile, user=request.user)
    selected_country = get_country(settings.DEFAULT_COUNTRY)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=profile)
        user_form = UserForm(request.POST, instance=profile)
        if profile_form.is_valid() and user_form.is_valid():
            # Get the current email address
            current_email = profile.user.email
            # Get the (potential) new email address
            new_email = request.POST.get('email')
            # If the addresses do not match, add a new address for the user,
            # and start listening for an email confirmation.  When the
            # confirmation is received, update the users email address and
            # delete any additional addresses
            if new_email != current_email:
                profile.add_email_address(
                    request, new_email)
            # Save the form data and set the message text
            profile_form.save()
            user_form.save()
            msg = 'Profile updated successfully'
            # If the current and new addresses don't mate, then call an extra
            # save to reset the email address value on the profile (this will
            # get updated correctly when the new address is confirmed)
            if new_email != current_email:
                profile.user.email = current_email
                profile.save()
                # Reset the user form object to ensure that the correct values
                # are displayed when the page reloads
                user_form = UserForm(instance=request.user)
                # update the message text
                msg = f'Profile updated successfully.\n  You requested a change\
                 in email address.  A confirmation request has been sent \
                    to:\n {new_email}\n  Please complete the confirmation to \
                    update your email address.'
            messages.success(
                request,
                msg,
                'from__update_profile'
            )
        else:
            messages.error(
                request,
                'Update failed.  Please ensure the form is valid.',
                'from__update_profile'
            )
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserForm(instance=request.user)
        selected_country = get_country(profile.default_country)

    # Get all orders, with the most recent first
    orders = profile.orders.all().order_by('-id')

    email_address_change_pending = (
        len(EmailAddress.objects.filter(user=request.user)) > 1)

    context = {
        'view': 'profile',
        'profile_form': profile_form,
        'user_form': user_form,
        'email_address_change_pending': email_address_change_pending,
        'orders': orders,
        'selected_country': selected_country
    }

    # https://stackoverflow.com/questions/19755102/django-allauth-change-user-email-with-without-verification#29661871
    if email_address_change_pending is True:
        pending_email_addresses = list(
            EmailAddress.objects.filter(
                user=request.user).exclude(primary=True))
        context['pending_email_addresses'] = pending_email_addresses

    return render(request, 'profiles/profile.html', context)


@login_required
def order_history(request, order_number):

    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    order = get_object_or_404(Order, order_number=order_number)

    messages.info(
        request,
        (
            f'This is a legacy confirmation for order number:\n {order_number}'
            '\nA confirmation email was sent on the order date.'
        ),
        'from__order_history_profile'
    )

    context = {
        'view': 'order_history',
        'order': order,
        'country_name': get_country(order.delivery_country)['name']
    }

    return render(request, 'checkout/order_details.html', context)
# ...............................................End Modified Boutique-Ado Code
