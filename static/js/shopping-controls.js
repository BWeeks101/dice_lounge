/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/

function initQuantityInput() {

    /* Rewritten from boutique ado sample project */

    // Disable +/- buttons when qty input value outside 2-9 range
    const handleEnableDisable = (itemId) => {
        $(`#qtyForm${itemId}`)[0].reportValidity();
        let value = parseInt($(`#qtyInput${itemId}`).val());
        $(`#decrementQty${itemId}`).prop('disabled', value < 2);
        $(`#incrementQty${itemId}`).prop('disabled', value > 9);
    };

    // Set initial disabled state of +/- buttons
    const initInputStates = () => {
        let allQtyInputs = $('.qty-input');
        $(allQtyInputs).each((i) => {
            handleEnableDisable($(allQtyInputs[i]).attr('data-item-id'));
        });
    };

    // Add event handlers to qty inputs and +/- buttons
    const addInputEventHandlers = () => {
        // Check enable/disable every time the qty input is changed
        $('.qty-input').on('input', (e) => {
            handleEnableDisable($(e.currentTarget).attr('data-item-id'));
        });

        // Increment/decrement qty input value when a +/- button is clicked
        $('.increment-qty, .decrement-qty').click((e) => {
            // Prevent the default click action
            e.preventDefault();
            // Get the itemId of the clicked button
            let itemId = $(e.currentTarget).attr('data-item-id');
            // Get the qty input element
            let qtyInput = $(`#qtyInput${itemId}`)[0];
            // Get the value of the qty input element
            let qtyInputVal = parseInt($(qtyInput).val());
            // If the current value of the input is NAN set the value to 1, then
            // update the enabled state of the +/- buttons and return
            if (Number.isNaN(qtyInputVal)) {
                $(qtyInput).val(1);
                handleEnableDisable(itemId);
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
            $(qtyInput).val(qtyInputVal);
            // Update the enabled state of the +/- buttons
            handleEnableDisable(itemId);
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