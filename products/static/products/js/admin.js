/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global disableDropdown, enableDropdown, getDropdownErrorState,
getDropdownDisabledState, addMask, hideMask, showMask, updateMask, isDomElem */


/* Update the reduced price display and the price/percentage input mask */
/* positions */
function updateReducedPrice() {
    if (!isDomElem($('#id_price'))) {
        return;
    }

    let price = parseFloat($('#id_price').val().
    trim());

    /* Update the position of the input mask for the price input */
    const updatePriceInputMask = (value) => {
        if (isNaN(value)) {
            hideMask($('#id_price'));
            return;
        }
        showMask($('#id_price'));
        updateMask($('#id_price'));
    };

    updatePriceInputMask(price);

    let reduction = parseFloat($('#id_reduced_percentage').val().
        trim());

    /* Update the position of the input mask for the reduced percentage input */
    const updatePercentageInputMask = (value) => {
        if (isNaN(value)) {
            hideMask($('#id_reduced_percentage'));
            return;
        }
        showMask($('#id_reduced_percentage'));
        updateMask($('#id_reduced_percentage'));
    };

    updatePercentageInputMask(reduction);

    let adjustedPrice = parseFloat(price - ((price / 100) * reduction));

    let selector = '#reducedPrice span.price-display, #reducedPrice ' +
        'span.price-currency ';
    if (isNaN(adjustedPrice)) {
        $(selector).removeClass('text-success').
            addClass('text-danger');
        $('#reducedPrice span.price-display').html('N/A');
        return;
    }

    $(selector).removeClass('text-danger').
            addClass('text-success');
    $('#reducedPrice span.price-display').html(adjustedPrice.toFixed(2));

}

/* Set input mask on price input */
function initPrice() {
    if (!isDomElem($('#id_price'))) {
        return;
    }

    // Create the input mask
    addMask({
        inputElem: $('#id_price'),
        extraClasses: ['number-input', 'form-control'],
        mask: '£',
        leadingMask: true
    });

    // Update the position of the mask and input text
    updateMask($('#id_price'));
}

/* Set initial state of the reduced price controls and add a change listener */
/* to the reduced checkbox */
function initReduced() {
    if (!isDomElem($('#id_reduced'))) {
        return;
    }

    // Initially disable the reduced percentage input
    $('#id_reduced_percentage').attr('disabled', true);

    const initPercentageInputMask = () => {
        addMask({
            inputElem: $('#id_reduced_percentage'),
            maskId: 'percentageInputMask',
            extraClasses: ['number-input', 'form-control'],
            mask: '%'
        });
        hideMask($('#id_reduced_percentage'));
    };

    initPercentageInputMask();

    /* Alter the disabled state of the reduced percentage and reduced reason */
    /* controls based on the state of the reduced checkbox */
    const toggleStateReducedReason = () => {
        // Get the state of the checkbox
        let isChecked = $('#id_reduced').prop('checked');

        // If checked, enable the controls and return
        let disabledState;
        if (isChecked) {
            disabledState = getDropdownDisabledState($('#id_reduced_reason'));
            if (disabledState.input === true) {
                $('#id_reduced_percentage').attr('disabled', false);
            }
            if (disabledState.toggle === true) {
                enableDropdown($('#id_reduced_reason'));
                $('#id_reduced_reason').closest('.dropdown').
                    addClass('border-dark').
                        removeClass('border-muted').
                            find('.dropdown-menu .dropdown-item:first-of-type').
                                click();
                updateReducedPrice();
                $('#reducedPrice').removeClass('d-none');
            }
            return;
        }

        // Otherwise disable the controls
        $('#id_reduced_percentage').attr('disabled', true).
            val('');
        disableDropdown($('#id_reduced_reason'));
        $('#id_reduced_reason').closest('.dropdown').
            addClass('border-muted').
                removeClass('border-dark').
                    find('.dropdown-toggle').
                        html('---------');
        $('#id_reduced_reason').val('');
        updateReducedPrice();
        $('#reducedPrice').addClass('d-none');
        hideMask($('#id_reduced_percentage'));
    };

    // Add a change listener to the reduced checkbox to toggle the state of the
    // reduced percentage and reduced reason controls
    $('#id_reduced').on('change', () => {
        toggleStateReducedReason();
    });

    // Add an input listener to the reduced_percentage input to update the
    // displayed adjusted price
    $('#id_price, #id_reduced_percentage').on('input change keyup', () => {
        updateReducedPrice();
    });
}

function initCoreSetScenics() {
    if (!isDomElem($('#id_core_set')) || !$('#id_scenics')) {
        return;
    }

    $('#id_core_set').on('change', () => {
        if ($('#id_core_set').prop('checked') === true &&
                $('#id_scenics').prop('checked') === true) {
            $('#id_scenics').prop('checked', false);
        }
    });

    $('#id_scenics').on('change', () => {
        if ($('#id_scenics').prop('checked') === true &&
                $('#id_core_set').prop('checked') === true) {
            $('#id_core_set').prop('checked', false);
        }
    });
}

/* Check the state of values before form submission */
function initForms() {

    const initProductAdminForm = () => {
        if (!isDomElem($('#productAdminForm'))) {
            return;
        }

        /* Validate the add product form before submission */
        $('#productAdminForm').on('submit', (e) => {
            // Prevent submission
            e.preventDefault();

            // Get the submit button and disable it
            $(e.currentTarget).find('button[type=submit]').
                attr('disabled', true);

            // Check if any dropdowns are displaying errors by iterating over
            // each dropdown and checking the error state
            let valid = true;
            $('.dropdown-wrapper input[type=hidden]').each((i, elem) => {
                // If valid is already false, then return
                if (valid === false) {
                    return;
                }

                // Check if the dropdown is displaying an error, and if so, set
                // valid to false
                if (getDropdownErrorState($(elem)) === true) {
                    valid = false;
                }
            });

            // If no dropdowns are displaying errors, continue
            if (valid === true) {
                // If the reduced percentage input is disabled, enable it (it is
                // required) and set it's value to 0
                if ($('#id_reduced_percentage').attr('disabled') &&
                        $('#id_reduced_percentage').
                            attr('disabled') !== false) {
                    $('#id_reduced_percentage').attr('disabled', false).
                        val('0');
                }

                // Remove the submission handler
                $(e.currentTarget).off('submit');

                // Submit the form
                $(e.currentTarget).submit();
            }

            // Otherwise the form is not valid, so get the submit button and
            // enable it
            $(e.currentTarget).find('button[type=submit]').
                attr('disabled', false);
        });
    };

    initProductAdminForm();
}

/* Add click listeners to product_management edit links */
function initEditButtons() {

    // Process the url of each button, removing the initial id attribute
    $('.edit-btn').each((i, elem) => {
        let url = $(elem).attr('href');
        url = (url.substring(0, (url.length - 1)));
        url = url.substring(0, url.lastIndexOf('/') + 1);
        $(elem).attr('href', url);
    });

    // Add click listeners to each button to open a url to edit the relevant
    // item
    $('.edit-btn').on('click', (e) => {
        // Prevent the default action
        e.preventDefault();

        // Get the associated element from the data-target attribute of the
        // selected button
        let target = $(e.currentTarget).attr('data-target');

        // Get the url from the href attribute of the selected button
        let url = $(e.currentTarget).attr('href');

        // Get the value of the target
        let value = $(target).val();

        // If the target is an admin list, get the value of the active
        // list-group-item instead
        if ($(target).hasClass('admin-list')) {
            value = $(target).find('.list-group-item.active').
                attr('data-value');
        }

        if (value === undefined ||
            isNaN(parseInt(value)) ||
                parseInt(value) < 0) {
            return;
        }

        // Add the value of the input to the url and open it
        url += value + '/';
        window.location = url;
    });
}

/* Set input mask on the default reduced percentage input */
function initDefaultReducedPercentage() {
    if (!isDomElem($('#id_default_reduction_percentage'))) {
        return;
    }

    addMask({
        inputElem: $('#id_default_reduction_percentage'),
        maskId: 'defaultReductionPercentageInputMask',
        extraClasses: ['number-input', 'form-control'],
        mask: '%'
    });

    $('#id_default_reduction_percentage').
        on('input change keyup focusout', () => {
            let val = $('#id_default_reduction_percentage').val();

            if (isNaN(parseInt(val))) {
                hideMask($('#id_default_reduction_percentage'));
                return;
            }
            showMask($('#id_default_reduction_percentage'));
            updateMask($('#id_default_reduction_percentage'));
        });
}

$(() => {
    initForms();
    initPrice();
    initReduced();
    initCoreSetScenics();
    initEditButtons();
    initDefaultReducedPercentage();
});