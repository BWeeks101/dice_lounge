/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global getValidationErrorHtml */

/* call the server to ensure we have a valid uk postcode */
function submitPostcode(postcodeInput, callback) {
    // No postcodeInput, so fire the callback (if it exists), or return.
    if ($(postcodeInput).length === 0) {
        if (callback) {
            return callback();
        }
        return;
    }

    // If the postcode input is disabled, set the isvalid data attribute to
    // true, then fire the callback or return.
    // (If the postcode input is disabled it won't be submitted, so no need to
    // validate)
    if ($(postcodeInput).attr('disabled')) {
        $(postcodeInput).attr('data-isvalid', true);
        if (callback) {
            return callback();
        }
        return;
    }

    // Get the error div for the input in question
    let errorDiv = $(postcodeInput).closest('div').
        next();

    // Setup the post data object.  Contains the csrf token and postcode to
    // be checked.
    let data = {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'postcode': $(postcodeInput).val()
    };

    // Validate the selection against the server
    $.post('/checkout/validate_postcode/', data, (response) => {
        $(errorDiv).html('');
        $(postcodeInput).attr('data-isvalid', true);
        // If the server did not return a response of true, display an error.
        if (response.result !== true) {
            $(postcodeInput).attr('data-isvalid', false);
            let msg = 'Please enter a valid UK postcode.';
            if (response.result === 'failed') {
                msg = 'Unable to validate postcode.  If your billing and ' +
                'delivery addresses are mainland UK please continue.  ' +
                'Otherwise, please call us to discuss.';
            }
            $(errorDiv).html(getValidationErrorHtml(msg));
        }
        // Otherwise, fire the callback or return
        if (callback) {
            return callback();
        }
    });
}

/* Initialise event handlers on postcode inputs and perform validation of */
/* initial values */
function initPostcodeInputs() {

    /* add 'debounced' input/focusout listeners to postcode inputs to handle */
    /* postcode validation */
    const initPostcodeEventHandlers = () => {
        let timer;

        // Half a second after input or focusout, validate the postcode
        $('.postcode-input').on('input focusout', (e) => {
            clearTimeout(timer);
            timer = setTimeout(() => {
                submitPostcode($(e.currentTarget));
            }, 500);
        });
    };

    initPostcodeEventHandlers();

    // Initial postcode validation
    $('.postcode-input').each((i, elem) => {
        if ($(elem).val().length > 0) {
            submitPostcode($(elem));
        }
    });
}

/* doc ready function */
$(() => {
    initPostcodeInputs();
});