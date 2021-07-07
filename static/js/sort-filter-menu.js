/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global initCollapsibleTogglerArrows */

/* Add click listener for sort/filter removal links */
function addSortFilterListeners() {

    /* Remove filter when clicking filter badge */
    $('.filter-badge').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the current url
        let currentUrl = new URL(window.location);

        // Get the filter and value
        let filter = $(e.currentTarget).attr('data-filter');
        let filterVal = $(e.currentTarget).attr('data-filter-value');

        // Locate the filter in the Url
        let currentVals = currentUrl.searchParams.get(filter).split(',');

        // Remove the filterVal from the list of values for the filter
        currentVals.splice(currentVals.indexOf(filterVal), 1);

        // Convert the list to a comma separated string
        currentVals = currentVals.toString();

        // Remove trailing comma
        if (currentVals.endsWith(',')) {
            currentVals = currentVals.substr(0, currentVals.length - 1);
        }

        // Update the url
        currentUrl.searchParams.set(filter, currentVals);

        // If currentVals is blank, remove the filter from the url
        if (!currentVals.length) {
            currentUrl.searchParams.delete(filter);
        }

        // Load the updated url
        window.location.replace(currentUrl);
    });

    /* Remove filter when clicking remove filter link/button */
    $('#remove-filter-link, button.remove-filters').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the current url
        let currentUrl = new URL(window.location);

        // Delete the sort and direction params from the url
        currentUrl.searchParams.delete("stock");
        currentUrl.searchParams.delete("category");
        currentUrl.searchParams.delete("genre");
        currentUrl.searchParams.delete("product_line");
        currentUrl.searchParams.delete("publisher");

        // Load the updated url
        window.location.replace(currentUrl);
    });

    /* Remove sort when clicking remove sort link */
    $('#remove-sort-link').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the current url
        let currentUrl = new URL(window.location);

        // Delete the sort and direction params from the url
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        // Load the updated url
        window.location.replace(currentUrl);
    });

    /* Remove filter and sort when clicking remove filter/sort link */
    $('#remove-filter-sort-link').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the current url
        let currentUrl = new URL(window.location);

        // Delete the sort and direction params from the url
        currentUrl.searchParams.delete("stock");
        currentUrl.searchParams.delete("category");
        currentUrl.searchParams.delete("genre");
        currentUrl.searchParams.delete("product_line");
        currentUrl.searchParams.delete("publisher");

        // Delete the sort and direction params from the url
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        // Load the updated url
        window.location.replace(currentUrl);
    });

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

    /* Apply a sort when clicking on sort-radio inputs */
    $('.sort-radio').on('click', (e) => {
        // Get the current url
        let currentUrl = new URL(window.location);

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
        // Get the filter values from the data-filters property of the button
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

        // Get the current url
        let currentUrl = new URL(window.location);

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

        // Load the updated url
        window.location.replace(currentUrl);
    });

    // Invert arrow on filter/sort collapse toggler when clicked
    let filterTogglerSelector = '#filterCollapseToggler, #sortCollapseToggler' +
        '#filterCollapseToggler_offcanvas, #sortCollapseToggler_offcanvas';
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

        Object.entries(filters).forEach(([filter, value]) => {
            $('#applyFilters').
                attr(`data-${filter}-filters`, value);
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
}

/* doc ready function */
$(() => {
    initSortFilterMenus();
});