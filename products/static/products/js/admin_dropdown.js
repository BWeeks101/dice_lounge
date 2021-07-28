/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global isDomElem, updateReducedPrice, hideMask, submitListRequest */

/* Ensure the clicked element was a dropdown-item */
function isDropdownClickValid(elem) {
    if (!isDomElem(elem)) {
        return false;
    }
    if (!$(elem).hasClass('dropdown-item')) {
        if (!$(elem).closest('dropdown-item').length > 0) {
            return false;
        }
    }
    return true;
}

/* Ensure the value of the dropdowns are set per the value of the */
/* respective hidden input */
function setAdminDropdownValues() {
    let hiddenInputs = $('.admin-dropdown input[type=hidden]');
    $(hiddenInputs).each((i, elem) => {
        $(elem).click();
    });
}

/* Initialise the admin selection dropdown */
function initAdminDropdowns() {

    /* Add click listeners to dropdown menus to update hidden input when a */
    /* child dropdown-item is clicked */
    $('.admin-dropdown .dropdown-menu').on('click', (e) => {
        // If a dropdown-item (or descendent of) was not the click target,
        // return
        if (!isDropdownClickValid($(e.target))) {
            return;
        }

        // Get the admin value
        let selectedVal = $(e.target).attr('data-value');

        // Get the hidden input
        let hiddenInput = $(e.target).closest('.dropdown').
                find('input[type=hidden]');

        // Update the value of the hidden input
        $(hiddenInput).closest('.dropdown').
            find('input[type=hidden]').
                val(selectedVal);

        // Remove the active class from .dropdown-items
        $(e.currentTarget).find('.dropdown-item.active').
                removeClass('active');

        // Set the current dropdown-item as active
        $(e.target).addClass('active');

        // Update the dropdown toggler text
        $(e.currentTarget).closest('.dropdown').
            find('a.dropdown-toggle').
                html($(e.target).html());
    });

    /* Add a click listener to the hidden input to simplify calling click */
    /* events */
    $('.admin-dropdown input[type=hidden]').on('click', (e) => {
        // Prevent the default action
        e.preventDefault();

        // Get the value of the input
        let value = $(e.currentTarget).val();

        let item;
        if (value && value.length > 0) {
            // Get the dropdown-item that has a matching data-value to the input
            item = $(e.currentTarget).closest('.dropdown').
                find(`.dropdown-menu .dropdown-item[data-value=${value}]`);
            // If we found a matching item, click it and return
            if (item.length > 0) {
                $(item).click();
                return;
            }
        }

        // No matching item, so find the active dropdown item
        let active = $(e.currentTarget).closest('.dropdown').
            find(`.dropdown-menu .dropdown-item.active`);
        // If we found an active item, click it and return
        if (active.length > 0) {
            $(active).click();
            return;
        }

        // No active item, so get the first dropdown item instead
        let first = $(e.currentTarget).closest('.dropdown').
            find(`.dropdown-menu .dropdown-item:first-of-type`);
        // If we found the first dropdown item, click it
        if (first.length > 0) {
            $(first).click();
        }
    });

    /* Ensure the initial value of the dropdowns are set per the value of the */
    /* respective hidden input */
    setAdminDropdownValues();
}

/* Disable a dropdown */
/* Requires: */
/*  hiddenInput: Object.  hidden input element within the dropdown wrapper */
function disableDropdown(hiddenInput) {
    // Disable the hidden input
    $(hiddenInput).attr('disabled', true);
    // Disable the dropdown toggler
    $(hiddenInput).closest('.dropdown').
        find('.dropdown-toggle').
            attr('disabled', true);
}

/* Enable a dropdown */
/* Requires: */
/*  hiddenInput: Object.  hidden input element within the dropdown wrapper */
function enableDropdown(hiddenInput) {
    // Enable the hidden input
    $(hiddenInput).attr('disabled', false);
    // Enable the dropdown toggler
    $(hiddenInput).closest('.dropdown').
        find('.dropdown-toggle').
            attr('disabled', false);
}

/* Get the disabled state of a dropdown */
/* Requires: */
/*  hiddenInput: Object.  hidden input element within the dropdown wrapper */
// eslint-disable-next-line no-unused-vars
function getDropdownDisabledState(hiddenInput) {
    let input = !$(hiddenInput).attr('disabled') === false;
    let toggle = !$(hiddenInput).closest('.dropdown').
        find('.dropdown-toggle').
            attr('disabled') === false;

    return {input, toggle};
}

/* Return the error state of a dropdown */
/* Requires: */
/*  hiddenInput: Object.  hidden input element within the dropdown wrapper */
function getDropdownErrorState(hiddenInput) {
    return !$(hiddenInput).closest('.dropdown-wrapper').
        find('.dropdown-error-message').
            hasClass('d-none');
}

/* Set dropdown loading message */
/* Requires: */
/*  hiddenInput: Object.  hidden input element within the dropdown wrapper */
function setDropdownLoadingMessage(hiddenInput) {
    $(hiddenInput).closest('.dropdown').
        find('.dropdown-toggle').
            html(
                `<span class="text-dark">Loading...</span>
                <span class="text-dark icon">
                    <i class="fas fa-sync-alt fa-spin"></i>
                </span>`
            );
}

/* Set dropdown loading error message */
/* Requires: */
/*  hiddenInput: Object.  hidden input element within the dropdown wrapper */
/* Optional: */
/*  toggleMessage: String.  Text to display in the toggler */
/*  errorMessage: String.  Text to display in the error message */
function setDropdownErrorMessage(hiddenInput, toggleMessage, errorMessage) {
    if (!toggleMessage) {
        toggleMessage = 'An error occurred...';
    }
    if (!errorMessage) {
        errorMessage = 'Unable to retrieve list data from the server.  ' +
            'Please reload the page and try again.';
    }
    $(hiddenInput).closest('.dropdown').
        find('.dropdown-toggle').
            html(
                `<span class="text-danger icon">
                    <i class="fas fa-exclamation"></i>
                </span>
                <span class="text-danger">${toggleMessage}</span>`
            );
    $(hiddenInput).closest('.dropdown-wrapper').
        find('.dropdown-error-message').
            html(`<span class="small text-danger">${errorMessage}</span>`).
                removeClass('d-none');
    $(hiddenInput).closest('.dropdown-wrapper').
        find('.dropdown-help-text').
            addClass('d-none');
}

/* Clear dropdown loading error message */
/* Requires: */
/*  hiddenInput: Object.  hidden input element within the dropdown wrapper */
function clearDropdownErrorMessage(hiddenInput) {
    $(hiddenInput).closest('.dropdown').
        find('.dropdown-toggle').
            html('');
    $(hiddenInput).closest('.dropdown-wrapper').
        find('.dropdown-error-message').
            html('').
                addClass('d-none');
    $(hiddenInput).closest('.dropdown-wrapper').
        find('.dropdown-help-text').
            removeClass('d-none');
}

/* Disable dropdown and display loading message prior to submitting post */
/* Requires: */
/*  hiddenInput: Object.  hidden input element within the dropdown wrapper */
function prePopDropdown(hiddenInput) {
    // Disable the dropdown
    disableDropdown($(hiddenInput));

    // Set loading message in the toggler
    setDropdownLoadingMessage($(hiddenInput));
}

/* Display error message and disable dropdown on post failure or error */
/* Requires: */
/*  hiddenInput: Object.  hidden input element within the dropdown wrapper */
/* Optional: */
/*  toggleMessage: String.  Text to display in the toggler */
/*  errorMessage: String.  Text to display in the error message */
function popDropdownFailure(hiddenInput, toggleMessage, errorMessage) {
    setDropdownErrorMessage($(hiddenInput), toggleMessage, errorMessage);
    disableDropdown($(hiddenInput));
}

/* Populate a dropdown menu using data returned from a server request */
/* Requires: */
/*  response: Response data from the server */
/*  hiddenInput: Object.  hidden input element within the dropdown wrapper */
/*  callback: Function.  Callback function to execute post completion */
function popDropdown(response, hiddenInput, callback) {
    // Clear any existing dropdown error message content
    clearDropdownErrorMessage($(hiddenInput));

    // Get the dropdown-menu to use as a target for the dropdown-items
    let menu = $(hiddenInput).closest('.dropdown').
        find('.dropdown-menu');
    // If the menu contains a dropdown-items-container, use this instead
    if ($(menu).find('.dropdown-items-container').length > 0) {
        menu = $(menu).find('.dropdown-items-container');
    }
    // Clear the contents of the menu element
    $(menu).html('');

    // If the response returned no objects, display the default error, fire the
    // callback and return
    if (response.length < 1) {
        popDropdownFailure($(hiddenInput));
        if (typeof callback === 'function') {
            return callback();
        }
        return;
    }

    // Iterate over the response
    response.forEach((obj, i) => {
        // generate the dropdown-item elem html
        let item = `<a href="#!" data-value="${response[i].id}" `;
        if (response[i].default_reduction_percentage) {
            item += 'data-percentage="' +
                `${response[i].default_reduction_percentage}" `;
        }
        item += 'class="dropdown-item';
        // If the hidden input has no value and this is the first response
        // object, set the hidden input value and give the dropdown-item the
        // active class
        if ($(hiddenInput).val().length < 1) {
            if (i === 0) {
                $(hiddenInput).val(response[i].id);
                item += ' active';
            }
        }
        // finalise the dropdown-item html string
        let itemText = response[i].name;
        if (response[i].hidden && response[i].hidden === true) {
            itemText += '<span class="icon icon-red"><i class="fas fa-ghost">' +
                '</i></span>';
        }
        item += `">${itemText}</a>`;
        // add the dropdown as a new child of the menu element
        $(menu).append(item);
    });

    // Enable the dropdown
    enableDropdown($(hiddenInput));
    // Call the click event on the active dropdown-item
    // $(menu).find('.dropdown-item.active').
    //     click();
    // Call the click event on the hidden input
    $(hiddenInput).click();

    // If we got a single response with an id of -1, there was an issue
    // returning a valid list from the server
    if (response.length === 1 && response[0].id === '-1') {
        popDropdownFailure(
            $(hiddenInput),
            response[0].name,
            response[0].error
        );
    }

    // Fire the callback, passing response as a parameter
    if (typeof callback === 'function') {
        return callback(response);
    }
}

/* Submit a post request to get data with which to populate a dropdown menu */
/* Requires: */
/*  hiddenInput: Object.  Hidden input element within the dropdown wrapper */
/*  lookupType: String.  Table to interrogate. */
/* Optional: */
/*  extraData: Object.  Additional key:value pairs to add to the post request */
/*  callback: Function.  Callback function to execute post completion */
function submitDropdownRequest({hiddenInput, lookupType, extraData, callback}) {
    // if hiddenInput elem does not exist in the dom, return
    if (isDomElem(hiddenInput) === false) {
        return;
    }

    // If lookupType is not a string, return
    if (typeof lookupType !== 'string' || lookupType.length < 1) {
        return;
    }

    // Disable the dropdown and set the loading message in the toggler
    prePopDropdown($(hiddenInput));

    // Define the post data object.  Contains csrf token.
    let data = {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
    };

    // if extraData is an object, merge it with the data object to add any
    // additional key:value pairs to the post request
    if (typeof extraData === 'object') {
        data = $.extend(data, extraData);
    }

    let url = `/products/get_lookup/${lookupType}/`;
    // Post the data object to the url, and handle the response
    $.post(url, data, (response) => {
        // If we get a response, populate the dropdown
        popDropdown(response, $(hiddenInput), callback);
    }).fail(() => {
        // If the post request fails, display an error
        popDropdownFailure(hiddenInput);
        if (typeof callback === 'function') {
            return callback();
        }
    });
}

/* Populate the product line and sub product line dropdown menus, and set an */
/* additional click listener to refresh the sub product line values */
function initProductLinePairedDropdown(productLine, subProductLine) {
    if (!isDomElem($(productLine))) {
        return;
    }

    /* Populate the child dropdown menu */
    const getSubProductLines = () => {
        if (!isDomElem($(subProductLine))) {
            return;
        }

        submitDropdownRequest({
            hiddenInput: $(subProductLine),
            lookupType: `sub_product_line`,
            extraData: {'product_line': $(productLine).val()}
        });
    };

    /* Add click listeners to the product line dropdown menu to update the */
    /* sub product line dropdown when a dropdown item is clicked */
    const addItemListeners = () => {
        if (!isDomElem($(subProductLine))) {
            return;
        }

        $(productLine).closest('.dropdown').
            find('.dropdown-menu').
                on('click', (e) => {
                    // If a dropdown-item (or descendent of) was not the click
                    // target, return
                    if (!isDropdownClickValid($(e.target))) {
                        return;
                    }
                    getSubProductLines();
                });
    };

    addItemListeners();

    /* Populate the product line dropdown menu */
    /* NB: This will in turn populate the sub product line dropdown menu */
    const getProductLines = () => {
        submitDropdownRequest({
            hiddenInput: $(productLine),
            lookupType: 'product_line'
        });
    };

    getProductLines();
}


/* Populate the product line and sub product line dropdown menus, and set an */
/* additional click listener to refresh the sub product line values */
function initProductLineDropdown() {
    initProductLinePairedDropdown(
        $('#id_product_line'), $('#id_sub_product_line'));
}

/* Populate the product line and sub product line dropdown menus, and set an */
/* additional click listener to refresh the sub product line values */
function initProductLineForProductsDropdown() {
    initProductLinePairedDropdown(
        $('#id_product_line_for_products'),
        $('#id_sub_product_line_for_products')
    );

    /* Add click listeners to the sub product line dropdown menu to update */
    /* the product list when a dropdown item is clicked */
    const addItemListeners = () => {
        if (!isDomElem($('#id_sub_product_line_for_products'))) {
            return;
        }

        $('#id_sub_product_line_for_products').closest('.dropdown').
            find('.dropdown-menu').
                on('click', (e) => {
                    // If a dropdown-item (or descendent of) was not the click
                    // target, return
                    if (!isDropdownClickValid($(e.target))) {
                        return;
                    }

                    // Disable the product line and sub product line dropdowns
                    // (will enable via callback once the list is populated)
                    disableDropdown($('#id_product_line_for_products'));
                    disableDropdown($('#id_sub_product_line_for_products'));

                    submitListRequest({
                        listElem: $('#productList'),
                        lookupType: 'product',
                        extraData: {'sub_product_line':
                                $('#id_sub_product_line_for_products').val()},
                        callback: () => {
                            enableDropdown($('#id_product_line_for_products'));
                            enableDropdown(
                                $('#id_sub_product_line_for_products'));
                        }
                    });
                });
    };

    addItemListeners();
}

/* Populate the product line solo variant dropdown menus */
function initProductLineSoloDropdown() {
    if (!isDomElem($('#id_product_line_solo'))) {
        return;
    }

    submitDropdownRequest({
        hiddenInput: $('#id_product_line_solo'),
        lookupType: 'product_line'
    });
}

/* Populate the reduced reason dropdown menu */
function initReducedReasonDropdown() {
    if (!isDomElem($('#id_reduced_reason'))) {
        return;
    }

    // If there is a value set for the reduced percentage, capture it
    let initPercentage = $('#id_reduced_percentage').val();

    /* If the reduced checkbox is checked, reset the reduced percentage value */
    /* (if any).  Otherwise, disable the dropdown and clear the reduced */
    /* reason and reduced percentage values */
    const disableReducedReason = (initPercentage) => {
        if ($('#id_reduced').prop('checked') === true) {
            $('#id_reduced_percentage').attr('disabled', false);
            $('#reducedPrice').removeClass('d-none');
            if (initPercentage && initPercentage > 0) {
                $('#id_reduced_percentage').val(initPercentage);
            }
            updateReducedPrice();
            return;
        }
        disableDropdown($('#id_reduced_reason'));
        $('#id_reduced_reason').closest('.dropdown').
            addClass('border-muted').
                removeClass('border-dark').
                    find('.dropdown-toggle').
                        html('---------');
        $('#id_reduced_reason').val('');
        $('#id_reduced_percentage').val('');
        updateReducedPrice();
        hideMask($('#id_reduced_percentage'));
        $('#reducedPrice').addClass('d-none');
    };

    // Regardless of the pop result, this dropdown should be disabled by default
    // unless the reduced checkbox is checked.
    // Pass a callback to disable the dropdown as appropriate once it has been
    // populated
    submitDropdownRequest({
        hiddenInput: $('#id_reduced_reason'),
        lookupType: 'reduced_reason',
        callback: () => disableReducedReason(initPercentage)
    });

    // Add a click listener to update value of the reduction percentage input
    $('#id_reduced_reason').closest('.dropdown').
        find('.dropdown-menu').
            on('click', (e) => {
                // If a dropdown-item (or descendent of) was not the click
                // target, return
                if (!isDropdownClickValid($(e.target))) {
                    return;
                }
                $('#id_reduced_percentage').val(
                    $(e.target).attr('data-percentage'));
                updateReducedPrice();
            });
}

/* Populate the reduced reason solo variant dropdown menus */
function initReducedReasonSoloDropdown() {
    if (!isDomElem($('#id_reduced_reason_solo'))) {
        return;
    }

    submitDropdownRequest({
        hiddenInput: $('#id_reduced_reason_solo'),
        lookupType: 'reduced_reason'
    });
}

/* Populate the stock state dropdown menu */
function initStockStateDropdown() {
    if (!isDomElem($('#id_stock_state'))) {
        return;
    }

    submitDropdownRequest({
        hiddenInput: $('#id_stock_state'),
        lookupType: 'stock_state'
    });
}

/* Validate the max_per_purchase value */
function initMaxPerPurchaseDropdown() {
    if (!isDomElem($('#id_max_per_purchase'))) {
        return;
    }

    /* Add click listener to dropdown menu to validate the selected value */
    /* when a child dropdown-item is clicked */
    $('#id_max_per_purchase').closest('.dropdown').
        find('.dropdown-menu').
            on('click', (e) => {
                // If a dropdown-item (or descendent of) was not the click
                // target, return
                if (!isDropdownClickValid($(e.target))) {
                    return;
                }
                // Get the default max per purchase value
                let maxPerPurchase = $('#id_max_per_purchase').
                    attr('data-max-per-purchase');
                // Get the value of the selected dropdown-item as an integer
                let value = parseInt($(e.target).attr('data-value'));
                // If the value is NaN, less than 1 or greater than the default
                // max per purchase value, then display an error and return
                if (isNaN(value) || value < 1 || value > maxPerPurchase) {
                    setDropdownErrorMessage(
                        $('#id_max_per_purchase'),
                        `Invalid value selected (${value}).`,
                        `Values should be between 1-${maxPerPurchase}.  If ` +
                        'this is not the case, please reload the page.'
                    );
                    return;
                }
                // Otherwise we have selected a valid value.  If an error is
                // currently displayed, get the toggle text, clear the error
                // then reset the toggle text
                if (getDropdownErrorState($('#id_max_per_purchase'))) {
                    // Get the current toggle text
                    let toggle = $('#maxPerPurchaseToggler').html();
                    // Clear any displayed errors
                    clearDropdownErrorMessage($('#id_max_per_purchase'));
                    // Reset the toggle text
                    $('#maxPerPurchaseToggler').html(toggle);
                }
            });
}

/* Populate the category dropdown menu */
function initCategoryDropdown() {
    if (!isDomElem($('#id_category'))) {
        return;
    }

    submitDropdownRequest({
        hiddenInput: $('#id_category'),
        lookupType: 'category'
    });
}

/* Populate the genre dropdown menu */
function initGenreDropdown() {
    if (!isDomElem($('#id_genre'))) {
        return;
    }

    submitDropdownRequest({
        hiddenInput: $('#id_genre'),
        lookupType: 'genre'
    });
}

/* Populate the publisher dropdown menu */
function initPublisherDropdown() {
    if (!isDomElem($('#id_publisher'))) {
        return;
    }

    submitDropdownRequest({
        hiddenInput: $('#id_publisher'),
        lookupType: 'publisher'
    });
}

/* doc ready function */
$(() => {
    initAdminDropdowns();
    initProductLineSoloDropdown();
    initProductLineDropdown();
    initProductLineForProductsDropdown();
    initReducedReasonDropdown();
    initReducedReasonSoloDropdown();
    initStockStateDropdown();
    initMaxPerPurchaseDropdown();
    initCategoryDropdown();
    initGenreDropdown();
    initPublisherDropdown();
});