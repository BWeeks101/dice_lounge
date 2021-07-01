/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/

function initQuantityInput() {
    // Disable +/- buttons outside 1-9 range
    const handleEnableDisable = (itemId) => {
        let currentValue = parseInt($(`#qtyInput${itemId}`).val());
        $(`#decrementQty${itemId}`).prop('disabled', currentValue < 2);
        $(`#incrementQty${itemId}`).prop('disabled', currentValue > 9);
    };

    // Ensure proper enabling/disabling of all inputs on page load
    let allQtyInputs = $('.qty-input');
    $(allQtyInputs).each((i) => {
        handleEnableDisable($(allQtyInputs[i]).attr('data-item-id'));
    });

    // Check enable/disable every time the input is changed
    $('.qty-input').on('input', (e) => {
        handleEnableDisable($(e.currentTarget).attr('data-item-id'));
    });

    // Get the input, and inc/dec the value
    const alterValue = (elem, value) => {
        let closestInput = $(elem).closest('.input-group').
            find('.qty-input')[0];
        $(closestInput).val(parseInt($(closestInput).val()) + value);
        handleEnableDisable($(elem).attr('data-item-id'));
    };

    // Increment/decrement quantity
    $('.increment-qty, .decrement-qty').click((e) => {
        e.preventDefault();
        let value = 1;
        if ($(e.currentTarget).hasClass('decrement-qty')) {
            value = -1;
        }
        alterValue(e.currentTarget, value);
    });
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