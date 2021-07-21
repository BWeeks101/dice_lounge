/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global createResizeListener */

/* Initialise quantity dropdown elements */
function initQuantityDropdown() {

    /* Update the value of the hidden quantity input element, then return an */
    /* obj containing the csrf token, submission url and quantity value */
    const updateQty = (elem) => {
        // Get the parent form element, csrf token, submission url and selected
        // qty value
        let form = $(elem).closest('.qty-form');
        let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken]').val();
        let url = $(form).attr('action');
        let quantity = $(elem).attr('data-value');

        // Set the value of the hidden input element to the selected qty value
        $(form).find('input[type="hidden"][name="quantity"]').
            val(quantity);

        // Set the value of the dropdown toggler elem to the selected qty value
        $(elem).closest('.dropdown').
            find('.dropdown-toggle').
                html(quantity);

        // Clear the active class from dropdown items
        $(elem).closest('.dropdown-menu').
            find('.dropdown-item.active').
                removeClass('active');

        // Set the active class on the selected dropdown item
        $(elem).addClass('active');

        // return the csrf token, submission url and qty value
        return {form, url, 'postData': {csrfmiddlewaretoken, quantity}};
    };

    /* Add click listeners to dropdown items to update quantity (no submit) */
    /* Used by .qty-dropdowns on product_detail view */
    $('.qty-dropdown.select-only .dropdown-item').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // update the qty stored in the hidden input element
        updateQty(e.currentTarget);
    });

    /* Add click listeners to dropdown items to update quantity and submit */
    /* Used by .qty-dropdowns on basket view */
    $('.qty-dropdown:not(.select-only) .dropdown-item').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // update the qty stored in the hidden input element
        let data = updateQty(e.currentTarget);

        // If the csrf token is not found we cannot submit, so return
        if (data.postData.csrfmiddlewaretoken === undefined ||
                data.postData.csrfmiddlewaretoken === '') {
            return;
        }

        // If the url is not found we cannot submit, so return
        if (data.url === undefined || data.url === '') {
            return;
        }

        // Submit the form instead of sending a POST request.
        $(data.form)[0].submit();
    });

    /* Add click listener to remove-item links to remove item from basket and */
    /* reload the page */
    $('.remove-item').click((e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the csrf token
        let csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken]').val();

        // If the token is not found we cannot POST, so return
        if (csrfmiddlewaretoken === undefined || csrfmiddlewaretoken === '') {
            return;
        }

        // Get the remove action url
        let url = $(e.currentTarget).attr('data-remove-url');

        // If the url is not found we cannot POST, so return
        if (url === undefined || url === '') {
            return;
        }

        // Send the POST request, then reload the page
        $.post(url, {csrfmiddlewaretoken}).done(() => {
            location.reload();
        });
    });
}

/* Initialise resizing of mobile block elements to maintain consistent width */
function initMobileCheckoutBlockAlignment() {

    // If the mobile block elems do not exist, return
    if ($('#total-mobile-block').length === 0 ||
            $('#checkout-buttons-mobile-block').length === 0) {
        return;
    }

    /* Set #total-mobile-block width = #checkout-buttons-mobile-block width */
    const setMobileBlockWidth = () => {
        $('#total-mobile-block').css('width',
            $('#checkout-buttons-mobile-block').css('width'));
    };

    setMobileBlockWidth();

    // Create a resize listener on the window, calling setMobileBlockWidth()
    createResizeListener(setMobileBlockWidth);
}

/* doc ready function */
$(() => {
    initQuantityDropdown();
    initMobileCheckoutBlockAlignment();
});