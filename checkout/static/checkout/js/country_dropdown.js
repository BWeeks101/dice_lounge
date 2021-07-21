/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global getValidationErrorHtml */

/* call the server to ensure we have a valid country selection */
function submitCountry(countryInput, callback) {
    if ($(countryInput).length === 0) {
        if (callback) {
            return callback();
        }
        return;
    }

    if ($(countryInput).attr('disabled')) {
        $(countryInput).attr('data-isvalid', true);
        if (callback) {
            return callback();
        }
        return;
    }

    let errorDiv = $(countryInput).closest('.dropdown-wrapper').
        parent().
            next();

    let data = {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'country_code': $(countryInput).val()
    };
    // Validate the selection against the server
    $.post(`/checkout/validate_country/`, data, (response) => {
        $(errorDiv).html('');
        $(countryInput).attr('data-isvalid', true);
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
        if (callback) {
            return callback();
        }
    });
}

/* Ensure the value of the dropdowns are set per the value of the */
/* respective hidden input */
function setCountryDropdownValues() {
    let dropdowns = $('.country-dropdown');
    $(dropdowns).each((i, elem) => {
        let input = $(elem).find('input[type=hidden]');
        let val = $(input).val();
        let item = $(elem).find(`.dropdown-item[data-value=${val}]`);
        if ($(item).length === 0) {
            $(elem).find('.dropdown-item.active').
                click();
            return;
        }
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