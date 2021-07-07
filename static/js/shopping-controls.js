/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global createResizeListener */

// function initQuantityInput() {

//     /* Rewritten from boutique ado sample project */


//     // Disable +/- buttons when qty input value outside 2-9 range
//     const handleEnableDisable = (productId) => {
//         let forms = $(`.qty-form[data-product-id=${productId}]`);
//         $(forms).each((i) => {
//             let form = forms[i];
//             form.reportValidity();
//             let value = $(form).
//                 find(`.qty-input[data-product-id=${productId}]`).
//                     val();
//             $(form).find(`.decrement-qty[data-product-id=${productId}]`).
//                 prop('disabled', value < 2);
//             $(form).find(`.increment-qty[data-product-id=${productId}]`).
//                 prop('disabled', value > 9);
//         });
//     };

//     // Set initial disabled state of +/- buttons
//     const initInputStates = () => {
//         let allQtyInputs = $('.qty-form');
//         $(allQtyInputs).each((i) => {
//             handleEnableDisable($(allQtyInputs[i]).attr('data-product-id'));
//         });
//     };

//     // Add event handlers to qty inputs and +/- buttons
//     const addInputEventHandlers = () => {
//         // Check enable/disable every time the qty input is changed
//         $('.qty-input').on('input', (e) => {
//             // Get the productId of the input element
//             let productId = $(e.currentTarget).attr('data-product-id');
//             $(`.qty-input[data-product-id=${productId}]`).
//                 val($(e.currentTarget).val());
//             handleEnableDisable($(e.currentTarget).attr('data-product-id'));
//         });

//         // Increment/decrement qty input value when a +/- button is clicked
//         $('.increment-qty, .decrement-qty').click((e) => {
//             // Prevent the default click action
//             e.preventDefault();
//             // Get the productId of the clicked button
//             let productId = $(e.currentTarget).attr('data-product-id');
//             // Get the value of the qty input element
//             let qtyInputVal = parseInt($(e.currentTarget).
//                 closest('.qty-input-container').
//                     find(`.qty-input[data-product-id=${productId}]`).
//                         val());
//             // If the current value of the input is NAN set the value to 1,
//             // then update the enabled state of the +/- buttons and return
//             if (Number.isNaN(qtyInputVal)) {
//                 $(`.qty-input[data-product-id=${productId}]`).val(1);
//                 handleEnableDisable(productId);
//                 return;
//             }
//             let modifier = 1;
//             // Set value to -1 if a - button was clicked
//             if ($(e.currentTarget).hasClass('decrement-qty')) {
//                 modifier = -1;
//             }
//             // Add the modifier to the qtyInputVal
//             qtyInputVal += modifier;
//             // Apply min/max values for qtyInputVal
//             if (qtyInputVal < 1) {
//                 qtyInputVal = 1;
//             } else if (qtyInputVal > 10) {
//                 qtyInputVal = 10;
//             }
//             // Update the qty input value
//             $(`.qty-input[data-product-id=${productId}]`).val(qtyInputVal);
//             // Update the enabled state of the +/- buttons
//             handleEnableDisable(productId);
//         });

//         // Update item quantity
//         $('.update-link').click((e) => {
//             e.preventDefault();
//             $(e.currentTarget).closest('.qty-form')[0].submit();
//         });

//         // Remove item from basket and reload
//         $('.remove-item').click((e) => {
//             e.preventDefault();
//             let csrfToken = $('[name=csrfmiddlewaretoken]').val();
//             if (csrfToken === undefined) {
//                 return;
//             }
//             let url = $(e.currentTarget).attr('data-remove-url');
//             let data = {'csrfmiddlewaretoken': csrfToken};

//             $.post(url, data).done(function() {
//                 location.reload();
//             });
//         });
//     };

//     initInputStates();
//     addInputEventHandlers();
// }

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

    /* Add click listeners to dropdown items to update quantity (no POST) */
    /* Used by .qty-dropdowns on product_detail view */
    $('.qty-dropdown.select-only .dropdown-item').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // update the qty stored in the hidden input element
        updateQty(e.currentTarget);
    });

    /* Add click listeners to dropdown items to update quantity and post */
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