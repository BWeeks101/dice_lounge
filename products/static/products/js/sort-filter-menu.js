/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global initCollapsibleTogglerArrows */

/* Add click listener for sort/filter removal links */
function addSortFilterListeners() {

    /* Remove filter when clicking remove filter button */
    $('button.remove-filters').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the current url
        let currentUrl = new URL(window.location);

        // Delete the filter params from the url
        currentUrl.searchParams.delete("stock");
        currentUrl.searchParams.delete("category");
        currentUrl.searchParams.delete("genre");
        currentUrl.searchParams.delete("product_line");
        currentUrl.searchParams.delete("publisher");

        // Load the updated url
        window.location.replace(currentUrl);
    });

    /* Get filter values from the data-filters property of the apply button */
    const getFilters = () => {
        let filters = [
            {
                value: $('#applyFilters').attr('data-product-line-filters'),
                param: 'product_line'
            },
            {
                value: $('#applyFilters').attr('data-genre-filters'),
                param: 'genre'
            },
            {
                value: $('#applyFilters').attr('data-publisher-filters'),
                param: 'publisher'
            },
            {
                value: $('#applyFilters').attr('data-category-filters'),
                param: 'category'
            },
            {
                value: $('#applyFilters').attr('data-stock-filters'),
                param: 'stock'
            }
        ];

        return filters;
    };

    /* Set apply-filters button enabled/disabled */
    const setApplyFiltersButtonState = (enabled) => {
        // If enabled is true, remove the disabled class from .apply-filters
        // buttons
        if (enabled === true) {
            $('.apply-filters').removeClass('disabled');
            return;
        }

        // Add the disabled class to .apply-filters buttons
        $('.apply-filters').addClass('disabled');
    };

    /* Check for unapplied filter values.  Returns true if there are */
    /* unapplied filters, otherwise false. */
    const checkFilters = () => {
        // Get filter values from the data-filters property of the apply button
        let filters = getFilters();

        // Get the current url
        let currentUrl = new URL(window.location);

        // Set a variable to indicate whether any filters are unapplied
        let unapplied = false;

        // Iterate over the filters array, comparing each filter value against
        // the same filter in the currentUrl.  If any do not match, set
        // unapplied = true.
        filters.forEach((filter) => {
            // Get the applied filter value from the url
            let appliedFilter = currentUrl.searchParams.get(filter.param);
            // Get the current filter from the filters array
            let currentFilter = filter.value;

            // If we have not yet found an unapplied filter
            if (unapplied === false) {
                // If the url filter value is not null, has a value length > 0
                // and the current filter has a length > 0
                if (appliedFilter !== null &&
                        appliedFilter.length > 0 && currentFilter.length > 0) {

                    // Convert both filter values into arrays, alphabetically
                    // sort them, then turn them back into strings
                    appliedFilter = currentUrl.searchParams.get(filter.param).
                        split(',').
                            sort().
                                toString();
                    currentFilter = filter.value.split(',').
                        sort().
                            toString();

                    // If the strings do not match after sorting then we have
                    // unapplied filters.  Set unapplied to true and return.
                    if (appliedFilter !== currentFilter) {
                        unapplied = true;
                    }
                    return;
                }

                // if the url filter does not exist but the current filter does
                // then set unapplied to true and return.
                if (appliedFilter === null && currentFilter.length > 0) {
                    unapplied = true;
                    return;
                }

                // If the url filter exists, but the length does not match the
                // length of the current filter (which should be 0 at this
                // point), set unapplied to true.
                if (appliedFilter !== null &&
                        appliedFilter.length !== currentFilter.length) {
                    unapplied = true;
                }
            }
        });

        return unapplied;
    };

    /* Get filter type from a filter checkbox/link element */
    const getFilterType = (elem) => {
        let elemType = 'link';
        if ($(elem).attr('type') === 'checkbox') {
            elemType = 'checkbox';
        }

        // Get the current filter type
        let filterType = 'category';
        let param;
        if ($(elem).hasClass(`genre-filter-${elemType}`)) {
            filterType = 'genre';
        } else if ($(elem).hasClass(`publisher-filter-${elemType}`)) {
            filterType = 'publisher';
        } else if ($(elem).hasClass(`stock-filter-${elemType}`)) {
            filterType = 'stock';
        } else if ($(elem).
                hasClass(`product-line-filter-${elemType}`)) {
            filterType = 'product-line';
            param = 'product_line';
        }

        if (param === undefined) {
            param = filterType;
        }
        // return the filter type
        return {
            type: filterType,
            param
        };
    };

    /* Add/update/remove filters to/from apply-filters button data attributes */
    /* Called when changing the state of a filter checkbox */
    const setFilterValue = (elem) => {
        // Get the checked state of the checkbox
        let isChecked = $(elem).prop('checked');

        // Get the filter value of the checkbox
        let filterVal = $(elem).attr('data-filter-value');

        // Set the checked state of any checkbox elements with the same
        // filterVal to match this element
        let pairedElems = $(`[type=checkbox][data-filter-value=${filterVal}]`);
        $(pairedElems).each((i, pElem) => {
            if (pElem !== elem && $(pElem).prop('checked') !== isChecked) {
                $(pElem).prop('checked', isChecked);
            }
        });

        // Get the current filter type
        let filterType = getFilterType(elem);

        // Get the stored filter values from the apply button
        let currentVals = $('#applyFilters').
            attr(`data-${filterType.type}-filters`);
        if (!currentVals) {
            currentVals = '';
        }
        currentVals = currentVals.split(',');

        // Locate the filterVal in the list of currentVals
        let filterValIndex = currentVals.indexOf(filterVal);

        // If the checkbox is checked and the filterVal is not present, add it
        // to the list
        if (isChecked) {
            if (filterValIndex === -1) {
                currentVals.unshift(filterVal);
            }
        }

        // If the checkbox is not checked and the filterVal is present, remove
        // it from the list
        if (!isChecked) {
            if (filterValIndex !== -1) {
                currentVals.splice(filterValIndex, 1);
            }
        }

        // Convert the list to a comma separated string
        currentVals = currentVals.toString();

        // Remove trailing comma if present
        if (currentVals.endsWith(',')) {
            currentVals = currentVals.substr(0, currentVals.length - 1);
        }

        // Overwrite the data-<filterType>-filters attribute of the
        // .apply-filters button with the new filter string
        $('#applyFilters').
            attr(`data-${filterType.type}-filters`, currentVals);

        setApplyFiltersButtonState(checkFilters());
    };

    /* Check/uncheck all child-checks when parent-check is checked/unchecked */
    $('.parent-check').on('click', (e) => {
        // Get the checked state of the parent-check
        let isChecked = $(e.currentTarget).prop('checked');

        // Get .child-check inputs
        let childInputs = $(e.currentTarget).parent().
            next().
                find('.child-check');

        // Set the checked state of each child-check to match that of the parent
        // and set the filter values appropriately
        $(childInputs).each((i) => {
            let elem = $(childInputs[i]);
            $(elem).prop('checked', isChecked);
            setFilterValue(elem);
        });
    });

    /* Check parent-check when any child-check is checked, or uncheck it when */
    /* all child-checks are unchecked */
    $('.child-check').on('click', (e) => {
        // Get child-check checked states
        let childInputs = $(e.currentTarget).parent().
            parent().
                find('.child-check');

        // If any child-check is checked set isChecked to true, otherwise it
        // will be false
        let isChecked = false;
        $(childInputs).each((i) => {
            let elem = $(childInputs[i]);
            if (isChecked === false) {
                isChecked = $(elem).prop('checked');
            }
        });

        // Get the parent-check element
        let parentInput = $(e.currentTarget).parent().
            parent().
                prev().
                    find('.parent-check')[0];

        // Set the parent-check checked state === isChecked
        $(parentInput).prop('checked', isChecked);

        // Update filter values for the parent-check
        setFilterValue(parentInput);
    });

    /* Pass clicked filter checkbox elem to setFilterValue() */
    let filterCheckboxSelector = '.category-filter-checkbox, ' +
        '.genre-filter-checkbox, .publisher-filter-checkbox, ' +
            '.stock-filter-checkbox, .product-line-filter-checkbox';
    $(filterCheckboxSelector).on('click', (e) => {
        setFilterValue(e.currentTarget);
    });

    /* Apply filter when clicking filter links in product card */
    let filterLinkSelector = '.category-filter-link, .stock-filter-link, ' +
        '.product-line-filter-link, .publisher-filter-link, .genre-filter-link';
    $(filterLinkSelector).on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the filter value of the link
        let filterVal = $(e.currentTarget).attr('data-filter-value');

        // Get the current filter type
        let filterType = getFilterType(e.currentTarget);

        // Get the current url
        let currentUrl = new URL(window.location);

        // If there is a filter of this type present, remove it
        currentUrl.searchParams.delete(filterType.param);

        // Update the url with the new filter
        currentUrl.searchParams.set(filterType.param, filterVal);

        // Load the updated url
        window.location.replace(currentUrl);
    });

    /* Update the current url with any unapplied filters, and return the */
    /* updated url */
    const addFiltersToUrl = () => {
        // Get the current url
        let currentUrl = new URL(window.location);

        // If there are no filters to apply, return the url
        if (checkFilters() === false) {
            return currentUrl;
        }

        // Get the filter values from the data-filters property of the button
        let filters = getFilters();

        // Iterate over the filters array
        filters.forEach((filter) => {
            // Remove the existing filter from the url
            currentUrl.searchParams.delete(filter.param);
            // If the filter value exists, update the url
            if (filter.value.length > 0) {
                currentUrl.searchParams.set(filter.param, filter.value);
            }
        });

        // Reset to page 1 of the results
        currentUrl.searchParams.delete('page');

        return currentUrl;
    };

    /* Apply a sort and any unapplied filters when clicking on sort-radio */
    /* inputs */
    $('.sort-radio').on('click', (e) => {

        // Get the current url and apply any unapplied filters
        let currentUrl = addFiltersToUrl();

        // Get the sort data
        let selectedVal = $(e.currentTarget).attr('value');

        // If the reset sort is selected update the url and refresh
        if (selectedVal === 'None_None') {
            // Delete the sort and delete params from the url
            currentUrl.searchParams.delete('sort');
            currentUrl.searchParams.delete('direction');

            // Reset the results to page 1
            currentUrl.searchParams.delete('page');

            // Load the updated url
            window.location.replace(currentUrl);
            return;
        }

        // Not the reset sort, so get the sort value and direction
        let sort = selectedVal.slice(0, selectedVal.lastIndexOf('_'));
        let direction = selectedVal.slice(selectedVal.lastIndexOf('_') + 1);

        // Update the url
        currentUrl.searchParams.set('sort', sort);
        currentUrl.searchParams.set('direction', direction);

        // Reset the results to page 1
        currentUrl.searchParams.delete('page');

        // Load the updated url
        window.location.replace(currentUrl);
    });

    /* Apply filters when clicking the apply filters button */
    $('button.apply-filters').on('click', () => {
        // If there are no filters to apply, return
        if (checkFilters() === false) {
            return;
        }

        //Update the filters in the current url
        let currentUrl = addFiltersToUrl();

        // Load the updated url
        window.location.replace(currentUrl);
    });

    // Invert arrow on filter/sort collapse toggler when clicked
    let filterTogglerSelector = '#filterCollapseToggler, ' +
        '#sortCollapseToggler, #filterCollapseToggler_offcanvas, ' +
        '#sortCollapseToggler_offcanvas';
    initCollapsibleTogglerArrows(filterTogglerSelector);

    /* Get active filters from checkboxes on load, and apply the values to */
    /* the data attributes of the apply filters button */
    const getInitialFilters = () => {
        // Get filter checkbox elements
        let selector = '.category-filter-checkbox[checked], ' +
            '.genre-filter-checkbox[checked], ' +
                '.publisher-filter-checkbox[checked], ' +
                    '.stock-filter-checkbox[checked], ' +
                        '.product-line-filter-checkbox[checked]';
        let filterCheckboxes = $(selector);

        // Create filters object
        let filters = {};

        // For each filter object
        $(filterCheckboxes).each((i, elem) => {
            // Get the filter value of the checkbox
            let filterVal = $(elem).attr('data-filter-value');

            // Get the filter type
            let filterType = getFilterType(elem);

            // If the value for the current type is blank, set the initial
            // value and return
            if (filters[filterType.type] === '' ||
                    filters[filterType.type] === undefined) {
                filters[filterType.type] = filterVal;
                return;
            }

            // Split the current filter values into an array
            let currentVals = filters[filterType.type].split(',');

            // Locate the filterVal in the array of currentVals
            let filterValIndex = currentVals.indexOf(filterVal);

            // If the filterVal is not present, add it
            if (filterValIndex === -1) {
                filters[filterType.type] += ',' + filterVal;
            }
        });

        // For each filter in the filters array, set the matching filter
        // data attribute value on the #applyFilters button.  If any value
        // length is > 0 then we have at least one applied filter, so remove
        // the disabled class from .remove-filters buttons
        Object.entries(filters).forEach(([filter, value]) => {
            $('#applyFilters').
                attr(`data-${filter}-filters`, value);
            if (value.length > 0) {
                $('.remove-filters').removeClass('disabled');
            }
        });
    };

    getInitialFilters();
}

/* Update unique property values for offcanvas elems to prevent duplication */
/* and set the active radio */
// eslint-disable-next-line no-unused-vars
function initSortFilterMenus() {

    /* Adjust unique attributes of .form-check-input elems within the */
    /* #sortFilterOffCanvas mobile sort/filter menu */
    $('#sortFilterOffCanvas .form-check-input').each((i, elem) => {
        // get the element id
        let elemid = $(elem).attr('id');

        // If the elemid has already been updated, return
        if (elemid.indexOf('_offcanvas') > -1) {
            return;
        }

        // Update the checkbox/radio id, and label 'for' attribute
        elemid += '_offcanvas';
        $(elem).attr('id', elemid);
        $(elem).next().
            attr('for', elemid);

        // If the element is a radio, update the name attribute of
        // the radio and the label
        if ($(elem).hasClass('sort-radio')) {
            $(elem).attr('name', 'sortRadiosOffCanvas');
            $(elem).next().
                attr('name', 'sortRadiosOffCanvas');
        }
    });

    // Adjust ids/targets of offcanvas collapse and apply/remove button elements
    $('#sortFilterOffCanvas #filterCollapse').
        attr('id', 'filterCollapse_offcanvas');
    $('#sortFilterOffCanvas #filterCollapseToggler').
        attr('id', 'filterCollapseToggler_offcanvas').
            attr('data-bs-target', '#filterCollapse_offcanvas');

    $('#sortFilterOffCanvas #applyFilters').
        attr('id', '#applyFilters_offcanvas');
    $('#sortFilterOffCanvas #removeFilters').
        attr('id', '#removeFilters_offcanvas');

    $('#sortFilterOffCanvas #sortCollapse').
        attr('id', 'sortCollapse_offcanvas');
    $('#sortFilterOffCanvas #sortCollapseToggler').
        attr('id', 'sortCollapseToggler_offcanvas').
            attr('data-bs-target', '#sortCollapse_offcanvas');

    // Iterate over radio buttons where the value matches the applied_sort
    // django template context value, and ensure the element is checked
    let appliedSort = $('#sortCollapse').attr('data-applied-sort');
    $(`.sort-radio[value="${appliedSort}"]`).each((i, elem) => {
        // If the element is already checked, return
        if ($(elem).attr('checked')) {
            return;
        }

        // Otherwise ensure the element is checked
        $(elem).attr('checked', true);
    });

    // Add listeners to sort/filter control elements
    addSortFilterListeners();

    // Iterate over all sort/filter inputs, and enable them
    let sortFilterSelector = '#filterCollapse .form-check-input, ' +
        '#sortCollapse .form-check-input, ' +
        '#sortFilterOffCanvas .form-check-input';
    $(sortFilterSelector).attr('disabled', false);
}

/* doc ready function */
$(() => {
    initSortFilterMenus();
});