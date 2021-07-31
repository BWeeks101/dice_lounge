/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global getValidationErrorHtml */

/* call the server to ensure we have a valid country selection */
function submitCountry(countryInput, callback) {
    // No countryInput, so fire the callback (if it exists), or return.
    if ($(countryInput).length === 0) {
        if (callback) {
            return callback();
        }
        return;
    }

    // If the country input is disabled, set the isvalid data attribute to true,
    // then fire the callback or return.
    // (If the countryInput is disabled it won't be submitted, so no need to
    // validate)
    if ($(countryInput).attr('disabled')) {
        $(countryInput).attr('data-isvalid', true);
        if (callback) {
            return callback();
        }
        return;
    }

    // Get the error div for the input in question
    let errorDiv = $(countryInput).closest('.dropdown-wrapper').
        parent().
            next();

    // Setup the post data object.  Contains the csrf token and country_code to
    // be checked.
    let data = {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'country_code': $(countryInput).val()
    };

    // Validate the selection against the server
    $.post(`/checkout/validate_country/`, data, (response) => {
        $(errorDiv).html('');
        $(countryInput).attr('data-isvalid', true);
        // If the server did not return a response of true, display an error.
        if (response.result !== true) {
            $(countryInput).attr('data-isvalid', false);
            let msg = 'Your selected country is not in our list of ' +
            'approved shipping destinations.  Please select another from ' +
            'the following list:';
            response.valid_countries.forEach((country) => {
                msg += `
                <br>${country.name}`;
            });
            $(errorDiv).html(getValidationErrorHtml(msg));
        }
        // Otherwise, fire the callback or return
        if (callback) {
            return callback();
        }
    });
}

/* Ensure the initial selected value of the dropdowns are set per the value */
/* of the respective hidden input */
function setCountryDropdownValues() {
    // Get the dropdowns
    let dropdowns = $('.country-dropdown');

    // Iterate over the dropdowns
    $(dropdowns).each((i, elem) => {
        // Get the associated hidden input
        let input = $(elem).find('input[type=hidden]');
        // Get the value of the hidden input
        let val = $(input).val();
        // Get dropdown items with a data-value attribute that matches the
        // value of the input
        let item = $(elem).find(`.dropdown-item[data-value=${val}]`);
        // If the items exist, look for one with the active class and click it
        if ($(item).length === 0) {
            $(elem).find('.dropdown-item.active').
                click();
            return;
        }
        // Otherwise, there is no active item, so click the returned item to
        // make sure at least one is active.
        $(item).click();
    });
}

/* Initialise the country selection dropdown */
// eslint-disable-next-line no-unused-vars
function initCountryDropdowns() {

    /* Add click listeners to dropdown items to update hidden country input */
    /* and validate the selection against the server */
    $('.country-dropdown .dropdown-item').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the country value
        let selectedVal = $(e.currentTarget).attr('data-value');

        // Get the hidden country input
        let countryInput = $(e.currentTarget).closest('.dropdown').
                find('input[type=hidden]');

        // Update the value of the hidden country input
        $(countryInput).closest('.dropdown').
            find('input[type=hidden]').
                val(selectedVal);

        // Remove the active class from .dropdown-items
        $(e.currentTarget).closest('.dropdown-menu').
            find('.dropdown-item.active').
                removeClass('active');

        // Set the current dropdown-item as active
        $(e.currentTarget).addClass('active');

        // Update the dropdown toggler text
        $(e.currentTarget).closest('.dropdown').
            find('a.dropdown-toggle').
                html($(e.currentTarget).html());

        // Validate the country selection
        submitCountry($(countryInput));
    });

    /* Ensure the initial value of the dropdowns are set per the value of the */
    /* respective hidden input */
    setCountryDropdownValues();
}

/* doc ready function */
$(() => {
    initCountryDropdowns();
});