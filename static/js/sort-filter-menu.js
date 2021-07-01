/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/

/* Add click listener for sort/filter removal links */
// eslint-disable-next-line no-unused-vars
function addSortFilterListeners() {
    // Remove filter when clicking filter badge
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

        if (!currentVals.length) {
            currentUrl.searchParams.delete(filter);
        }

        // Load the updated url
        window.location.replace(currentUrl);
    });

    // Remove filter when clicking remove filter link/button
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

    // Remove sort when clicking remove sort link
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

    // Remove filter and sort when clicking remove filter/sort link
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

    // add/update/remove filters to/from apply-filters button data attributes
    const setFilterValue = (elem) => {
        // Get the checked state of the checkbox
        let isChecked = $(elem).prop('checked');

        // Get the filter value of the checkbox
        let filterVal = $(elem).attr('data-filter-value');

        // Get the current filter type
        let filterType = 'category';
        if ($(elem).hasClass('genre-filter-checkbox')) {
            filterType = 'genre';
        } else if ($(elem).hasClass('publisher-filter-checkbox')) {
            filterType = 'publisher';
        } else if ($(elem).hasClass('stock-filter-checkbox')) {
            filterType = 'stock';
        } else if ($(elem).hasClass(
                'product-line-filter-checkbox')) {
            filterType = 'product-line';
        }

        // Get the stored filter values from the apply button
        let currentVals = $('#applyFilters').
            attr(`data-${filterType}-filters`);
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
            attr(`data-${filterType}-filters`, currentVals);
    };

    // Check/uncheck all child-checks when parent-check is checked/unchecked
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

    // Check parent-check when any child-check is checked, or uncheck it when
    // all child-checks are unchecked
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

    // Pass clicked filter checkbox elem to setFilterValue()
    let filterCheckboxSelector = '.category-filter-checkbox, ' +
        '.genre-filter-checkbox, .publisher-filter-checkbox, ' +
            '.stock-filter-checkbox, .product-line-filter-checkbox';
    $(filterCheckboxSelector).on('click', (e) => {
        setFilterValue(e.currentTarget);
    });

    // Apply filter when clicking filter links in product card
    let filterLinkSelector = '.category-filter-link, .stock-filter-link, ' +
        '.product-line-filter-link, .publisher-filter-link, .genre-filter-link';
    $(filterLinkSelector).on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the filter value of the link
        let filterVal = $(e.currentTarget).attr('data-filter-value');

        // Get the current filter type
        let filterType = 'category';
        if ($(e.currentTarget).hasClass('genre-filter-link')) {
            filterType = 'genre';
        } else if ($(e.currentTarget).hasClass('stock-filter-link')) {
            filterType = 'stock';
        } else if ($(e.currentTarget).
                hasClass('product-line-filter-link')) {
            filterType = 'product_line';
        } else if ($(e.currentTarget).hasClass('publisher-filter-link')) {
            filterType = 'publisher';
        }

        // Get the current url
        let currentUrl = new URL(window.location);

        // If there is a filter of this type present, remove it
        currentUrl.searchParams.delete(filterType);

        // Update the url with the new filter
        currentUrl.searchParams.set(filterType, filterVal);

        // Load the updated url
        window.location.replace(currentUrl);
    });

    // Apply a sort when clicking on sort-radio inputs
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

    // Apply filters when clicking the apply filters button
    $('button.apply-filters').on('click', () => {
        // Get the filter value from the data-filters property of the button
        let filters = {
            category: $('#applyFilters').attr('data-category-filters'),
            genre: $('#applyFilters').attr('data-genre-filters'),
            publisher: $('#applyFilters').attr('data-publisher-filters'),
            stock: $('#applyFilters').attr('data-stock-filters'),
            productLine: $('#applyFilters').attr('data-product-line-filters')
        };

        // Get the current url
        let currentUrl = new URL(window.location);

        // Remove the existing category/stock params from the url
        currentUrl.searchParams.delete('category');
        currentUrl.searchParams.delete('genre');
        currentUrl.searchParams.delete('publisher');
        currentUrl.searchParams.delete('stock');
        currentUrl.searchParams.delete('product_line');

        // If category filters contains a valid string
        if (filters.category.length > 0) {
            // update the url
            currentUrl.searchParams.set('category', filters.category);
        }

        // If genre filters contains a valid string
        if (filters.genre.length > 0) {
            // update the url
            currentUrl.searchParams.set('genre', filters.genre);
        }

        // If publisher filters contains a valid string
        if (filters.publisher.length > 0) {
            // update the url
            currentUrl.searchParams.set('publisher', filters.publisher);
        }

        // If stock filters contains a valid string
        if (filters.stock.length > 0) {
            // update the url
            currentUrl.searchParams.set('stock', filters.stock);
        }

        // If product-line filters contains a valid string
        if (filters.productLine.length > 0) {
            // update the url
            currentUrl.searchParams.set('product_line', filters.productLine);
        }

        // Reset to page 1 of the results
        currentUrl.searchParams.delete('page');

        // Load the updated url
        window.location.replace(currentUrl);
    });

    // Invert arrow on filter/sort collapse toggler when clicked
    let filterTogglerSelector = '#filterCollapseToggler, #sortCollapseToggler' +
        '#filterCollapseToggler_offcanvas, #sortCollapseToggler_offcanvas';
    $(filterTogglerSelector).on('click', (e) => {
        if ($(e.currentTarget).hasClass('collapsed')) {
            $(e.currentTarget).removeClass('dropdown-toggle-inverted').
                addClass('dropdown-toggle');
            return;
        }
        $(e.currentTarget).removeClass('dropdown-toggle').
            addClass('dropdown-toggle-inverted');
    });

    // Get active filters from checkboxes, and apply the values to the data
    // attributes of the apply filters button
    const getInitialFilters = () => {
        let selector = '.category-filter-checkbox[checked], ' +
            '.genre-filter-checkbox[checked], ' +
                '.publisher-filter-checkbox[checked], ' +
                    '.stock-filter-checkbox[checked], ' +
                        '.product-line-filter-checkbox[checked]';
        let filterCheckboxes = $(selector);
        let filters = {
            category: '',
            genre: '',
            publisher: '',
            stock: '',
            productLine: ''
        };

        $(filterCheckboxes).each((i) => {
            // Get the filter value of the checkbox
            let filterVal = $(filterCheckboxes[i]).attr('data-filter-value');

            // Get the filter type
            let filterType = 'category';
            if ($(filterCheckboxes[i]).hasClass('genre-filter-checkbox')) {
                filterType = 'genre';
            } else if ($(filterCheckboxes[i]).
                    hasClass('publisher-filter-checkbox')) {
                filterType = 'publisher';
            } else if ($(filterCheckboxes[i]).
                    hasClass('stock-filter-checkbox')) {
                filterType = 'stock';
            } else if ($(filterCheckboxes[i]).
                    hasClass('product-line-filter-checkbox')) {
                filterType = 'productLine';
            }

            // If the value for the current type is blank, set the initial
            // value and return
            if (filters[filterType] === '' ||
                    filters[filterType] === undefined) {
                filters[filterType] = filterVal;
                return;
            }

            // Split the current filter values into an array
            let currentVals = filters[filterType].split(',');

            // Locate the filterVal in the array of currentVals
            let filterValIndex = currentVals.indexOf(filterVal);

            // If the filterVal is not present, add it
            if (filterValIndex === -1) {
                filters[filterType] += ',' + filterVal;
            }
        });

        // Add the filter values to the apply filters button data attributes
        $('#applyFilters').
            attr('data-category-filters', filters.category).
                attr('data-genre-filters', filters.genre).
                    attr('data-publisher-filters', filters.publisher).
                        attr('data-stock-filters', filters.stock).
                            attr(
                                'data-product-line-filters',
                                filters.productLine
                            );
    };

    getInitialFilters();
}

/* Update unique property values for offcanvas elems to prevent duplication */
/* Set the active radio */
// eslint-disable-next-line no-unused-vars
function initSortFilterMenus(appliedSort) {
    // Adjust unique attributes of .form-check-input elems within the
    // OffCanvas mobile sort/filter menu
    $('.offcanvas-body .form-check-input').each((i) => {
        // get elem manually to avoid unused i variable linting error
        let elem = $('.offcanvas-body .form-check-input')[i];

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
    $('.offcanvas-body #filterCollapse').attr('id', 'filterCollapse_offcanvas');
    $('.offcanvas-body #filterCollapseToggler').
        attr('id', 'filterCollapseToggler_offcanvas').
            attr('data-bs-target', '#filterCollapse_offcanvas');

    $('.offcanvas-body #applyFilters').attr('id', '#applyFilters_offcanvas');
    $('.offcanvas-body #removeFilters').attr('id', '#removeFilters_offcanvas');

    $('.offcanvas-body #sortCollapse').attr('id', 'sortCollapse_offcanvas');
    $('.offcanvas-body #sortCollapseToggler').
        attr('id', 'sortCollapseToggler_offcanvas').
            attr('data-bs-target', '#sortCollapse_offcanvas');

    // Iterate over radio buttons the value matches the applied_sort
    // value, and ensure the element is checked
    $(`.sort-radio[value="${appliedSort}"]`).each((i) => {
        // get elem manually to avoid unused i variable linting error
        let elem = $(`.sort-radio[value="${appliedSort}"]`)[i];

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