/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/

function initQuantityInput() {

    /* Rewritten from boutique ado sample project */


    // Disable +/- buttons when qty input value outside 2-9 range
    const handleEnableDisable = (productId) => {
        let forms = $(`.qty-form[data-product-id=${productId}]`);
        $(forms).each((i) => {
            let form = forms[i];
            form.reportValidity();
            let value = $(form).
                find(`.qty-input[data-product-id=${productId}]`).
                    val();
            $(form).find(`.decrement-qty[data-product-id=${productId}]`).
                prop('disabled', value < 2);
            $(form).find(`.increment-qty[data-product-id=${productId}]`).
                prop('disabled', value > 9);
        });
    };

    // Set initial disabled state of +/- buttons
    const initInputStates = () => {
        let allQtyInputs = $('.qty-form');
        $(allQtyInputs).each((i) => {
            handleEnableDisable($(allQtyInputs[i]).attr('data-product-id'));
        });
    };

    // Add event handlers to qty inputs and +/- buttons
    const addInputEventHandlers = () => {
        // Check enable/disable every time the qty input is changed
        $('.qty-input').on('input', (e) => {
            // Get the productId of the input element
            let productId = $(e.currentTarget).attr('data-product-id');
            $(`.qty-input[data-product-id=${productId}]`).
                val($(e.currentTarget).val());
            handleEnableDisable($(e.currentTarget).attr('data-product-id'));
        });

        // Increment/decrement qty input value when a +/- button is clicked
        $('.increment-qty, .decrement-qty').click((e) => {
            // Prevent the default click action
            e.preventDefault();
            // Get the productId of the clicked button
            let productId = $(e.currentTarget).attr('data-product-id');
            // Get the value of the qty input element
            let qtyInputVal = parseInt($(e.currentTarget).
                closest('.qty-input-container').
                    find(`.qty-input[data-product-id=${productId}]`).
                        val());
            // If the current value of the input is NAN set the value to 1, then
            // update the enabled state of the +/- buttons and return
            if (Number.isNaN(qtyInputVal)) {
                $(`.qty-input[data-product-id=${productId}]`).val(1);
                handleEnableDisable(productId);
                return;
            }
            let modifier = 1;
            // Set value to -1 if a - button was clicked
            if ($(e.currentTarget).hasClass('decrement-qty')) {
                modifier = -1;
            }
            // Add the modifier to the qtyInputVal
            qtyInputVal += modifier;
            // Apply min/max values for qtyInputVal
            if (qtyInputVal < 1) {
                qtyInputVal = 1;
            } else if (qtyInputVal > 10) {
                qtyInputVal = 10;
            }
            // Update the qty input value
            $(`.qty-input[data-product-id=${productId}]`).val(qtyInputVal);
            // Update the enabled state of the +/- buttons
            handleEnableDisable(productId);
        });

        // Update item quantity
        $('.update-link').click((e) => {
            e.preventDefault();
            $(e.currentTarget).closest('.qty-form')[0].submit();
        });

        // Remove item from basket and reload
        $('.remove-item').click((e) => {
            e.preventDefault();
            let csrfToken = $('[name=csrfmiddlewaretoken]').val();
            if (csrfToken === undefined) {
                return;
            }
            let url = $(e.currentTarget).attr('data-remove-url');
            let data = {'csrfmiddlewaretoken': csrfToken};

            $.post(url, data).done(function() {
                location.reload();
            });
        });
    };

    initInputStates();
    addInputEventHandlers();
}

// ensure .disabled links do not function
function disableLinks() {
    // Remove existing click listeners
    $('a.disabled').off('click');

    // Add click listener which prevents the default action
    $('a.disabled').on('click', (e) => {
        e.preventDefault();
    });
}

$(function() {
    disableLinks();
    initQuantityInput();
});