/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global bootstrap */

/* Initialise the Sort dropdown */
/*
Requires:   dropDownToggler of type:
                String: element id based selector for the dropdown-toggler elem
            OR:
                Object: dropdown-toggler DOM elem object or jQuery object
*/
// function initSortDropdown(dropDownToggler) {

//     // If dropDownToggler is neither an object or string, return false
//     if (typeof dropDownToggler !== 'object' &&
//             typeof dropDownToggler !== 'string') {
//         return false;
//     }

//     /* Validate an object */
//     /*
//     Requires:   obj: Object to be validated
//     Returns:    false: Object is null, or a 0 length jQuery object
//                 true: Object is a jQuery object with length > 0
//                 dom: Object is not null, and not a jQuery object
//     */
//     const validObj = (obj) => {
//         // Object is null
//         if (obj === null) {
//             return false;
//         }

//         // JQ Object
//         if (length in obj) {

//             // 0 length
//             if (!obj.length) {
//                 return false;
//             }

//             // valid length
//             return true;
//         }

//         // Otherwise valid DOM object
//         return 'dom';
//     };

//     // If dropDownToggler is a string, ensure that it is formatted as an id
//     // based selector, including the dropdown-toggle class. Then create a
//     // jQuery object with this selector
//     if (typeof dropDownToggler === 'string') {
//         // Expecting an id, so ensure the first character is a #
//         if (dropDownToggler[0] !== '#') {
//             dropDownToggler = '#' + dropDownToggler;
//         }
//         // Object requires the .dropdown-toggle class, so ensure it is
//         // included
//         if (dropDownToggler.indexOf('.dropdown-toggle') === -1) {
//             dropDownToggler += '.dropdown-toggle';
//         }
//         // Create a jq object using the string as a selector
//         dropDownToggler = $(dropDownToggler);
//     }

//     let isValid;
//     // If dropDownToggler is an object, ensure that it is a valid jQuery
//     // object with the dropdown-toggle class
//     if (typeof dropDownToggler === 'object') {
//         isValid = validObj(dropDownToggler);

//         // If dropDownToggler is not valid, return false
//         if (!isValid) {
//             return false;
//         }

//         // If dropDownToggler is a DOM object, convert it to a JQ object
//         if (isValid === 'dom') {
//             dropDownToggler = $(dropDownToggler);
//         }

//         // Otherwise we have a valid JQ object so check it is a
//         // dropdown-toggler
//         dropDownToggler = $(dropDownToggler).filter('.dropdown-toggle');

//         // Final test for validation after filtering for .dropdown-toggle
//         // class
//         if (!validObj(dropDownToggler)) {
//             return false;
//         }
//     }

//     // Get the dropdown-wrapper ancestor
//     let dropDownWrapper = $(dropDownToggler).closest('.dropdown-wrapper');
//     // If no dropdown-menu is found, return false
//     if (!validObj(dropDownWrapper)) {
//         return false;
//     }

//     // Get the dropdown-menu sibling
//     let dropDownMenu = $(dropDownToggler).siblings('.dropdown-menu');
//     // If no dropdown-menu is found, return false
//     if (!validObj(dropDownMenu)) {
//         return false;
//     }

//     // Get the dropdown-items child elements from the dropdown-menu
//     let dropDownItems = $(dropDownMenu).children('.dropdown-item');
//     // If no dropdown-items are found, return false
//     if (!validObj(dropDownItems)) {
//         return false;
//     }

//     /* Set the dropdown text based on the active dropdown-item */
//     const setDropDownTogglerText = () => {
//         // Get the active dropdown item (if it exists)
//         let active = $(dropDownItems).filter('.active');
//         if (validObj(active)) {
//             // Set the visible text of the toggler to that of the active
//             // dropdown item
//             $(dropDownToggler).html($(active).html());
//         }
//     };

//     /* Add click listeners to dropdown items to apply sort */
//     const addDropDownItemListeners = () => {
//         $(dropDownItems).on('click', (e) => {
//             // prevent the default link click action
//             e.preventDefault();

//             // Get the current url
//             let currentUrl = new URL(window.location);

//             // Get the filter data
//             let selectedVal = $(e.currentTarget).attr('data-value');

//             // If the reset filter is selected update the url and refresh
//             if (selectedVal === 'None_None') {
//                 // Delete the sort and delete params from the url
//                 currentUrl.searchParams.delete('sort');
//                 currentUrl.searchParams.delete('direction');

//                 // Reset the results to page 1
//                 currentUrl.searchParams.delete('page');

//                 // Load the updated url
//                 window.location.replace(currentUrl);
//                 return;
//             }

//             // Not the reset filter, so get the filter sort and direction
//             let sort = selectedVal.slice(0, selectedVal.lastIndexOf('_'));
//             let direction = selectedVal.
//                    slice(selectedVal.lastIndexOf('_') + 1);

//             // Update the url
//             currentUrl.searchParams.set('sort', sort);
//             currentUrl.searchParams.set('direction', direction);

//             // Reset the results to page 1
//             currentUrl.searchParams.delete('page');

//             // Load the updated url
//             window.location.replace(currentUrl);
//         });
//     };

//     /* Resize the dropdown elements to maintain consistent size */
//     /*
//     Optional:   refreshTogglerText (Boolean).
//                 If true, calls setDropDownTogglerText() (default = false)
//     */
//     const resizeDropDownToggler = (refreshTogglerText = false) => {

//         // If refreshTogglerText is true, call setDropDownTogglerText()
//         if (refreshTogglerText) {
//             setDropDownTogglerText();
//         }
//         // console.log('refreshTogglerText: ' + refreshTogglerText);


//         /* Get the index of the widest dropdown-item */
//         /* Set dropdown-toggler text = widest dropdown-item text */
//         /* Return the width of the dropdown-toggler and reset the text */
//         const getDropDownTogglerWidth = () => {
//             let scrollWidth;
//             let outerWidth;
//             let currentText;

//             /* Get the id of the widest dropdown-item */
//             const getWidestDropDownItem = () => {
//                 let widestItemWidth;
//                 let widestItem;

//                 // Ensure the dropdown-menu is visible to allow accurate
//                 // calculation of child element widths
//                 $(dropDownMenu).addClass('force-show');

//                 // Ensure the dropdown-items are inline-block with no width
//                 // value to allow accurate calculation of their widths
//                 $(dropDownItems).addClass('fit-content');

//                 // For each dropdown-item, get the larger value of the
//                 // scrollWidth and the jQuery calculated outerWidth.  Store
//                 // the largest overall value from all dropdown-items, and the
//                 // item index.
//                 $(dropDownItems).each((i) => {
//                     if (!widestItemWidth) {
//                         widestItemWidth = 0;
//                     }
//                     scrollWidth = dropDownItems[i].scrollWidth;
//                     outerWidth = $(dropDownItems[i]).outerWidth();
//                     if (scrollWidth > outerWidth) {
//                         outerWidth = scrollWidth;
//                     }
//                     if (outerWidth > widestItemWidth) {
//                         widestItemWidth = outerWidth;
//                         widestItem = i;
//                     }
//                 });

//                 // Remove extra classes
//                 $(dropDownItems).removeClass('fit-content');
//                 $(dropDownMenu).removeClass('force-show');

//                 // Return the index of the widest dropdown-item
//                 return widestItem;
//             };
//             let widestItem = getWidestDropDownItem();

//             // If we have a widestItem, store the current dropdown-toggler
//             // text, then set the text of the dropdown-toggler to that of the
//             // widest item
//             if (widestItem) {
//                 currentText = $(dropDownToggler).html();
//                 $(dropDownToggler).html($(dropDownItems[widestItem]).html());
//             }

//             // Ensure the dropdown-toggler is visible, inline-block and with
//             // no width value to allow accurate width calculation
//             $(dropDownToggler).addClass('force-show fit-content');

//             // Get the scrollWidth and the jQuery calculated outerWidth
//             scrollWidth = dropDownToggler[0].scrollWidth;
//             outerWidth = $(dropDownToggler).outerWidth();

//             // Remove extra classes
//             $(dropDownToggler).removeClass('force-show fit-content');

//             // If currentText is populated, reset the dropdown-toggler text
//             // to currentText
//             if (currentText) {
//                 $(dropDownToggler).html(currentText);
//             }

//             // Return the larger value of the scrollWidth and the jQuery
//             // calculated outerWidth
//             if (scrollWidth > outerWidth) {
//                 outerWidth = scrollWidth;
//             }
//             return outerWidth;
//         };
//         let dropDownTogglerWidth = getDropDownTogglerWidth();
//         // console.log('t: ' + dropDownTogglerWidth);

//         // Set the maximum possible width = dropdown-wrapper parent width
//         let maxWidth = $(dropDownWrapper).parent().
//             width();
//         // console.log('mw: ' + maxWidth);

//         // Get combined dropdown-menu left + right border width
//         let dropDownMenuBorder = parseFloat(
//             $(dropDownMenu).css('border-left-width'));
//         dropDownMenuBorder += parseFloat(
//             $(dropDownMenu).css('border-right-width'));
//         // console.log('mb: ' + dropDownMenuBorder);

//         // Ensure dropdown-toggler width + dropdown-menu border does not
//         // exceed maxWidth
//         if ((dropDownTogglerWidth + dropDownMenuBorder) > maxWidth) {
//             dropDownTogglerWidth = (maxWidth - dropDownMenuBorder);
//         }
//         // console.log('nt: ' + dropDownTogglerWidth);

//         // Set dropdown-menu innerWidth to width of dropdown-toggler
//         $(dropDownMenu).innerWidth(dropDownTogglerWidth + 'px');

//         // Get dropdown-menu outerWidth after innerWidth resize
//         let dropDownMenuWidth = $(dropDownMenu).outerWidth();
//         // console.log('m: ' + dropDownMenuWidth);

//         // Set dropdown-wrapper outerWidth = dropdown-menu outerWidth
//         $(dropDownWrapper).outerWidth(dropDownMenuWidth + 'px');

//         // Get dropdown-wrapper width after resize (debug only)
//         // let dropDownWrapperWidth = $(dropDownWrapper).outerWidth();
//         // console.log('w: ' + dropDownWrapperWidth);
//     };

//     // Observe dropdown-items for innerHtml change and call resizeToggler()
//     const addResizeObservers = () => {
//         let observer = new MutationObserver(
//             () => resizeDropDownToggler(true));
//         $(dropDownItems).each((i) => {
//             observer.observe($(dropDownItems)[i], {
//                 childList: true,
//                 subtree: true,
//                 characterData: true
//             });
//         });
//     };

//     // Add an onresize handler to the window calling resizeToggler()
//     const addResizeListener = () => {
//         $(window).on('resize', () => {
//             resizeDropDownToggler();
//         });
//     };

//     // Display the dropdown-wrapper
//     const displayDropDownWrapper = () => {
//         $(dropDownWrapper).removeClass('d-none');
//     };

//     // Display the dropdown-wrapper
//     displayDropDownWrapper();
//     // Perform an initial resize of the dropdown-toggler and set the text
//     resizeDropDownToggler(true);
//     // Initialise the dropdown-item mutation observers
//     addResizeObservers();
//     // Initialise the window resize event handler
//     addResizeListener();
//     // Add click listeners to dropdown-items
//     addDropDownItemListeners();
// }

/* Create an intersection observer on the #scrollTopAnchor element, executing */
/* callbacks when intersecting (at top of page) or not intersecting (not top) */
/* Requires: */
/*      notTopAction: function.  Callback function executed when scrolled */
/*                    away from the top of the page */
/*      topAction: function.  Callback function executed when scrolled to the */
/*                 top of the page */
/* https://css-tricks.com/styling-based-on-scroll-position/ */
function initIntersectionObserver({notTopAction, topAction}) {
    if (
        "IntersectionObserver" in window &&
        "IntersectionObserverEntry" in window &&
        "intersectionRatio" in window.IntersectionObserverEntry.prototype
    ) {
        let observer = new IntersectionObserver((entries) => {
            if (entries[0].boundingClientRect.y < 0) {
                notTopAction();
            } else {
                topAction();
            }
        });
        observer.observe(document.querySelector("#scrollTopAnchor"));
    }
}

/* Create a resize listener on the window, passing the callback param */
/* Requires: */
/*      callback: callback function */
// eslint-disable-next-line no-unused-vars
function createResizeListener(callback) {
    if (callback === undefined || typeof callback !== 'function') {
        return;
    }

    let timer;

    // Modified from https://css-tricks.com/snippets/jquery/done-resizing-event/
    // On window resize, clear any existing timeout for the timer var, create
    // a new timeout for the timer var with a delay of a 5th of a second,
    // with callback() as a callback.  The callback will therefore
    // only be executed if no window resize event is called within the
    // timeout window.
    $(window).on('resize', () => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            callback();
        }, 200);
    });
}

/* ensure .disabled links do not function */
function disableLinks() {
    // Remove existing click listeners
    $('a.disabled').off('click');

    /* Add click listener which prevents the default action */
    $('a.disabled').on('click', (e) => {
        e.preventDefault();
    });
}

/* Add/remove box shadows for search/page input box containers */
function initInputBoxShadows() {

    /* search input focus */
    $('.search-input-container input').on('focus', (e) => {
        $(e.currentTarget).closest('.search-input-container').
            addClass('input-container-box-shadow');
    });

    /* search input focusout */
    $('.search-input-container input').on('focusout', (e) => {
        $(e.currentTarget).closest('.search-input-container').
            removeClass('input-container-box-shadow');
    });

    /* search button click */
    $('.search-input-container button').on('click', (e) => {
        $(e.currentTarget).closest('.search-input-container').
            addClass('input-container-box-shadow');
    });

    /* page input focus */
    $('.page-input-container > .page-input').on('focus', (e) => {
        $(e.currentTarget).closest('.page-input-container').
            addClass('input-container-box-shadow');
    });

    /* page input focusout */
    $('.page-input-container > .page-input').on('focusout', (e) => {
        $(e.currentTarget).closest('.page-input-container').
            removeClass('input-container-box-shadow');
    });

    /* page input button click */
    $('.page-input-container > .page-input-btn').on('click', (e) => {
        $(e.currentTarget).closest('.page-input-container').
            addClass('input-container-box-shadow');
    });

    // /* qty input focus */
    // $('.qty-input-container > input[type=number]').on('focus', (e) => {
    //     $(e.currentTarget).closest('.qty-input-container').
    //         addClass('input-container-box-shadow');
    // });

    // /* qty input focusout */
    // $('.qty-input-container > input[type=number]').on('focusout', (e) => {
    //     $(e.currentTarget).closest('.qty-input-container').
    //         removeClass('input-container-box-shadow');
    // });

    // /* qty input click */
    // $('.qty-input-container > input[type=number]').on('click', (e) => {
    //     $(e.currentTarget).closest('.qty-input-container').
    //         addClass('input-container-box-shadow');
    // });
}

/* Invert arrow on collapsible toggler click */
/* Requires: */
/*      selector: string.  collapsible toggler element selector. */
// eslint-disable-next-line no-unused-vars
function initCollapsibleTogglerArrows(selector) {
    $(selector).on('click', (e) => {
        if ($(e.currentTarget).hasClass('collapsed')) {
            $(e.currentTarget).removeClass('dropdown-toggle-inverted').
                addClass('dropdown-toggle');
            return;
        }
        $(e.currentTarget).removeClass('dropdown-toggle').
            addClass('dropdown-toggle-inverted');
    });
}

/* Add click listener to Back to Top button */
function initBackToTopButton() {

    // Show the btt button
    const showBtt = () => {
        $('button.btt-button').css('visibility', 'initial').
            css('opacity', '1');
    };

    // Hide the btt button
    const hideBtt = () => {
        $('button.btt-button').css('visibility', 'hidden').
            css('opacity', '0');
    };

    // Initialise an intersection observer to show/hide the btt button base on
    // scroll position
    initIntersectionObserver({notTopAction: showBtt, topAction: hideBtt});

    /* Add click listener to btt buttons to scroll the page to the top */
    $('button.btt-button, button.filter-btt-button').on('click', () => {
        window.scrollTo(0, 0);
    });
}

/* Set product card heights and create window resize listener to call again */
function initProductCardHeightAdjust() {

    /* Calculate and set heights for .product-name and .card-footer elements */
    const setProductCardHeights = () => {
        // Get the window width
        let windowWidth = window.outerWidth;

        // Get all .card-footer elements
        let cards = $('.product-container .card .card-footer');
        let colCount;
        let rows = [];

        // Determine the number of columns in a row
        // (widths based on bootstrap breakpoints)
        if (windowWidth >= 1400) { // xxl
            colCount = 6;
            if ($('#productContainer h2[data-view="all_games"]').length) {
                colCount = 4;
            }
        } else if (windowWidth >= 1200) { // xl
            colCount = 4;
        } else if (windowWidth >= 992) { // lg
            colCount = 3;
        } else if (windowWidth >= 768) { // md
            colCount = 2;
        } else if (windowWidth >= 576) { // sm
            colCount = 2;
        } else { // xs
            colCount = 1;
        }

        // If colCount is 1, remove any inline height value for all
        // .product-name and .card-footer elements, and return
        if (colCount === 1) {
            $(cards).each((i) => {
                $(cards[i]).find($('.product-name, .product-line-name')).
                    css('height', '');
                $(cards[i]).css('height', '');
            });
            return;
        }

        /* Populate the rows array with objects corresponding to rows of */
        /* product cards as displayed */
        /* Each object contains an array of product card footer and name */
        /* elems in that row */
        const buildRows = (colId) => {
            if (!colId) {
                colId = 0;
            }

            // Create row object with single cols array property
            let row = {
                'cols': []
            };

            /* Populate the cols array property of the current row object */
            const buildRow = () => {
                // If the length of the cols property is less than the colCount:
                // Add the element from the cards jq object that corresponds to
                // the colId, increment the colId, then if we are not at the end
                // of the cards jq object, ptc buildRow()
                if (row.cols.length < colCount) {
                    row.cols.push($(cards[colId]));
                    colId += 1;
                    if (colId < $(cards).length) {
                        return buildRow();
                    }
                }
            };

            // Call buildRow to finalise the current row object
            buildRow();

            // Add the row object to the end of the rows array
            rows.push(row);

            // If we have not reached the last element in the cards jq object,
            // ptc buildRows() passing the current colId
            if (colId < $(cards).length) {
                return buildRows(colId);
            }
        };

        // Call buildRows to finalise the rows array
        buildRows();

        // Iterate over the rows array
        rows.forEach((row) => {
            let nameHeight = 0;
            let footerHeight = 0;
            // Iterate over the cols array in the current row, getting the
            // height of the tallest .product-name and .card-footer in the row
            row.cols.forEach((col) => {
                // Locate the product name elem for this col, remove any inline
                // height value, then get the height + padding
                let nHeight = $(col).
                    find($('.product-name, .product-line-name')).
                        css('height', '').
                            innerHeight();
                // If the height is greater than the value of nameHeight, update
                // the value of nameHeight
                if (nHeight > nameHeight) {
                    nameHeight = nHeight;
                }

                // Remove any inline height value for the .card-footer, then get
                // the height + padding (minus the .product-name height)
                let fHeight = $(col).css('height', '').
                    innerHeight() - nHeight;
                // if the height is greater than the value of footer height,
                // update the value of footerHeight
                if (fHeight > footerHeight) {
                    footerHeight = fHeight;
                }
            });

            // Iterate over the cols array in the current row, setting the
            // height of each product name and card-footer elem to that of the
            // largest recorded value for each
            row.cols.forEach((col) => {
                $(col).find($('.product-name, .product-line-name')).
                    css('height', nameHeight);
                $(col).css('height', footerHeight + nameHeight);
            });
        });
    };

    setProductCardHeights();

    // Create a resize listener on the window, calling setProductCardHeights()
    createResizeListener(setProductCardHeights);
}

/* Initialise Toasts */
function initToasts() {
    // Create a toast instance for each .toast element and store them in an
    // array
    let toasts = [].slice.call(document.querySelectorAll('.toast')).
        map((toastEl) => new bootstrap.Toast(toastEl));

    // Iterate over the toasts array
    toasts.forEach((toast) => {
        // show the toast
        toast.show();

        /* Add an event listener to the hidden event for each toast. */
        /* When a toast is hidden, hide each other toast with the same */
        /* data-toast-id attribute value */
        // eslint-disable-next-line no-underscore-dangle
        toast._element.addEventListener('hidden.bs.toast', (e) => {
            // Get the data-toast-id value from the hidden element
            let toastId = $(e.currentTarget).attr('data-toast-id');

            // For each element with a matching data-toast-id and the .show
            // class, get the bootstrap toast instance and call the hide()
            // function
            $(`.toast[data-toast-id=${toastId}].show`).each((i, elem) => {
                bootstrap.Toast.getInstance(elem).hide();
            });
        });
    });
}

/* doc ready function */
$(() => {
    // Ensure disabled links do not function
    disableLinks();

    // Add event listeners to search/page input box containers
    initInputBoxShadows();

    // Initialise the Back to Top buttons
    initBackToTopButton();

    // Set product card heights, and create resize listener to call again
    initProductCardHeightAdjust();

    // Initialise Toasts
    initToasts();
});