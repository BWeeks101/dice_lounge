/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global submitPostcode, submitCountry,  getValidationErrorHtml*/

/* Contents of this file modified and expanded from the boutique-ado sample */
/* project */

/* eslint-disable new-cap */
/* eslint-disable no-undef */
/* eslint-disable camelcase */
/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here:
    https://stripe.com/docs/stripe-js
*/

function initUseBillingAddressCheckbox() {
    // Show/hide delivery inputs
    $('#id-use-billing-address').on('click', (e) => {
        // Get delivery inputs
        let deliveryInputs = $(
            '#deliveryAddressFieldset input:not([type=checkbox]), ' +
            '#deliveryCountryContainer, #deliveryNameRow'
        );
        // If the checkbox is checked, hide and disable the delivery inputs to
        // prevent them being submitted, and return.
        if ($(e.currentTarget).prop('checked') === true) {
            $(deliveryInputs).addClass('d-none').
                attr('disabled', true);
            $('#delivery_postcode-errors').html('');
            $('#delivery_country-errors').html('');
            return;
        }

        // Show and enable the delivery inputs, and reset their values to match
        // the billing inputs.  Ensure the country dropdowns are set correctly.
        $(deliveryInputs).removeClass('d-none').
            attr('disabled', false);
        $('#id_delivery_first_name').val($('#id_first_name').val());
        $('#id_delivery_last_name').val($('#id_last_name').val());
        $('#id_delivery_address1').val($('#id_street_address1').val());
        $('#id_delivery_address2').val($('#id_street_address2').val());
        $('#id_delivery_town_or_city').val($('#id_town_or_city').val());
        $('#id_delivery_county').val($('#id_county').val());
        $('#id_delivery_postcode').val($('#id_postcode').val());
        $('#id_delivery_country').val($('#id_country').val());
        setCountryDropdownValues();
    });

    // Ensure checkbox state is on by default
    $('#id-use-billing-address').prop('checked', true);
}

function initStripeElements() {

    /* ............................................Modified Boutique-Ado Code */
    let stripePublicKey = $('#id_stripe_public_key').text().
        slice(1, -1);
    let stripe = Stripe(stripePublicKey);
    let elements = stripe.elements();
    let style = {
        base: {
            color: '#212529', // Bootstrap 5 Dark
            fontFamily: '"Noto Sans", "Noto Sans JP", sans-serif', // Site fonts
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#6c757d' // Bootstrap 5 text-muted
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };
    let card = elements.create('card', {style, hidePostalCode: true});

    card.mount('#card-element');

    // Handle realtime validation errors on the card element
    card.addEventListener('change', (e) => {
        let errorDiv = $('#card-errors');
        if (e.error) {
            $(errorDiv).html(getValidationErrorHtml(e.error.message));
        } else {
            $(errorDiv).html('');
        }
    });

    return {stripe, card};

    /* ........................................End Modified Boutique-Ado Code */
}

/* Handle postcode/country validation prior to payment form submission, along */
/* with payment form submission itself */
function initPaymentForm(stripeObjs) {

    // Email address change requires confirmation.  Allowing users to change
    // Email at the order stage is messy.  This is disabled on the back end.
    // Mask the email input with a disabled input, that will display a
    // Notification if clicked
    const noEmailChangeFromCheckout = () => {
        let form = document.getElementById('payment-form');

        let email = $.trim(form.email.value);
        if (email.length > 0) {
            $('#id_email').attr('type', 'hidden');
            $('#id_email').wrap('<span id="email_wrapper"></span>');
            $('#email_wrapper').append('<input id="fake_email" ' +
                'class="stripe-style-input emailinput form-control ' +
                'border-muted text-muted" ' +
                `value="${email}" type="email" disabled>`);
            $('#email_wrapper').append('<div class="mb-3 text-info d-none" ' +
                'id="fake_email_notification">*' +
                'If you wish to change your Email address, please do so ' +
                'from your Profile before ordering</div>');
            $('#email_wrapper').on('click', () => {
                $('#fake_email_notification').removeClass('d-none');
            });
        }
    };

    noEmailChangeFromCheckout();

    /* Enable/disable card/submit button, fade payment form/loading overlay */
    const disableAndFadeElems = (disabled = true) => {
        const cardAndSubmitButton = () => {
            stripeObjs.card.update({disabled});
            $('.submit-button button[type=submit]').attr('disabled', disabled);
        };

        const fadePaymentForm = () => {
            $('#payment-form').fadeToggle(100);
        };

        const fadeLoadingOverlay = () => {
            $('#loading-overlay').fadeToggle(100);
        };

        // prior to form submission disable the card and submit button, fade the
        // payment form out and fade the overlay in, then return
        if (disabled === true) {
            cardAndSubmitButton();
            fadePaymentForm();
            fadeLoadingOverlay();
            return;
        }

        // submission failed without page reload (postcode/country are invalid).
        // Fade the overlay out, fade the payment form in, then enable the card
        // and submit button
        fadeLoadingOverlay();
        fadePaymentForm();
        cardAndSubmitButton();
    };

    /* Handle payment form submission */
    const submitForm = () => {
        // If the postcode/country are not valid, return
        if ($('input[data-isvalid=false]').length > 0) {
            disableAndFadeElems(false);
            return;
        }

        /* ........................................Modified Boutique-Ado Code */

        // Get the payment form element
        let form = document.getElementById('payment-form');

        // Get billing and delivery names from the form
        billing_first_name = $.trim(form.first_name.value);
        billing_last_name = $.trim(form.last_name.value);
        delivery_first_name = $.trim(form.first_name.value);
        delivery_last_name = $.trim(form.last_name.value);

        if ($('#id-use-billing-address').prop('checked') === false) {
            delivery_first_name = (
                $.trim(form.delivery_first_name.value));
            delivery_last_name = (
                $.trim(form.delivery_last_name.value));
        }

        // Create the data object to pass values on submission
        let data = {
            // csrf token
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            // stripe client secret key
            'client_secret': $('#id_client_secret').text().
                slice(1, -1),
            // checked state of save-info checkbox expressed as boolean
            'save_info': Boolean($('#id-save-info').attr('checked')),
            // billing/delivery name data - we will use this to aid the webhook
            // in finding/creating the order object. (Stripe otherwise only
            // holds a combined name field, which we would have to guess at how
            // to split.  This is more accurate.)
            billing_first_name,
            billing_last_name,
            delivery_first_name,
            delivery_last_name
        };

        // Post the data object to update the stripe payment intent with cached
        // checkout data
        $.post('/checkout/cache_checkout_data/', data).
            // Successfully posted, so proceed to card payment
            done(() => {
                // Create payment and delivery details object
                details = {
                    payment_method: {
                        'card': stripeObjs.card,
                        billing_details: {
                            name: ($.trim(form.first_name.value) +
                                    ' ' + $.trim(form.last_name.value)),
                            phone: $.trim(form.phone_number.value),
                            email: $.trim(form.email.value),
                            address: {
                                line1: $.trim(form.street_address1.value),
                                line2: $.trim(form.street_address2.value),
                                city: $.trim(form.town_or_city.value),
                                country: $.trim(form.country.value),
                                state: $.trim(form.county.value),
                                postal_code: $.trim(form.postcode.value)
                            }
                        }
                    }
                };

        /* ....................................End Modified Boutique-Ado Code */
                // By default, delivery name and address match billing details
                details.shipping = {
                    name: details.payment_method.billing_details.name,
                    address: details.payment_method.billing_details.address
                };

                // If the 'use billing address' checkbox is unchecked, use the
                // values from the delivery inputs for delivery instead
                if ($('#id-use-billing-address').prop('checked') === false) {
                    details.shipping.name = (
                        $.trim(form.delivery_first_name.value) + ' ' +
                        $.trim(form.delivery_last_name.value)
                    );
                    details.shipping.address = {
                        line1: $.trim(form.delivery_address1.value),
                        line2: $.trim(form.delivery_address2.value),
                        city: $.trim(form.delivery_town_or_city.value),
                        state: $.trim(form.delivery_county.value),
                        postal_code: $.trim(form.delivery_postcode.value),
                        country: $.trim(form.delivery_country.value)
                    };
                }

            /* ....................................Modified Boutique-Ado Code */

                // Submit the details to stripe for payment confirmation
                stripeObjs.stripe.
                    confirmCardPayment(data.client_secret, details).
                        then((result) => {
                            if (result.error) {
                                // If stripe returns an error, display it on the
                                // page
                                $('#card-errors').html(
                                    getValidationErrorHtml(
                                            result.error.message));
                                disableAndFadeElems(false);
                            } else if (
                                result.paymentIntent.status === 'succeeded') {
                                // Otherwise submit the payment form to the
                                // server to continue the order process
                                form.submit();
                            }
                        });
            }).
            // Unable to post, so reload the page.  Any errors will be displayed
            // as toasts via django messages from the server
            fail(() => {
                location.reload();
            });

            /* ................................End Modified Boutique-Ado Code */
    };

    $('#payment-form').on('submit', (e) => {
        e.preventDefault();
        disableAndFadeElems();

        // Chain submitPostcode->submitCountry->submitForm to ensure the form
        // is not submitted when postcode/country are not valid
        // (Chaining the callbacks ensures each async server call completes
        // before proceeding)
        submitPostcode(
            $('#id_postcode'),
            () => submitPostcode(
                $('#id_delivery_postcode'),
                () => submitCountry(
                    $('#id_country'),
                    () => submitCountry(
                        $('#id_delivery_country'),
                        submitForm
                    )
                )
            )
        );
    });
}

/* doc ready function */
$(() => {
    initUseBillingAddressCheckbox();
    initPaymentForm(initStripeElements());
});