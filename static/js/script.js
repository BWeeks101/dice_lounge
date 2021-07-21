/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global bootstrap */

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

/* Check if an object is a valid dom element. */
/* Refactored from the original source: */
/* http://stackoverflow.com/questions/28287499/ddg#28287642 */
/* Authored by: */
/* https://stackoverflow.com/users/1680836/war10ck */
function isDomElem(obj) {

    /* If elem is a jQuery object with length > 0, or an HTMLElement, return */
    /* true.  Otherwise return false. */
    const checkInstance = (elem = obj) => {
        if ((elem instanceof jQuery && elem.length) ||
                elem instanceof HTMLElement) {
            return true;
        }
        return false;
    };

    /* Iterate over an HTMLCollection.  Pass each object in the collection to */
    /* checkInstance().  If any return false, then false.  Otherwise return */
    /* true. */
    const iterateCollection = (i = 0) => {
        // If object at position i returns false, then return false
        if (!checkInstance(obj[i])) {
            return false;
        }
        // Increment i
        i += 1;
        // If not at the end of the collection check the next object
        if (i < obj.length) {
            return iterateCollection(i);
        }
        // Otherwise return true
        return true;
    };

    // If obj is an HTMLCollection with a length > 0, return the result of
    // iterateCollection()
    if (obj instanceof HTMLCollection && obj.length) {
        return iterateCollection();
    }

    // return the result of checkInstance()
    return checkInstance();
}

/* Returns a string containing error message html, formatted for */
/* checkout/profile payment/address forms */
/* Requires: */
/*  msg: String containing error text */
// eslint-disable-next-line no-unused-vars
function getValidationErrorHtml(msg) {
    let icon = `
        <span class="icon" role="alert">
            <i class="fas fa-times"></i>
        </span>
    `;
    msg = `<span>${msg}</span>`;
    return icon + msg;
}

/* Create a resize observer on an element, passing the callback param */
/* Requires: */
/*  elem: element to observe */
/*  callback: callback function */
function createResizeObserver(elem, callback) {
    if (callback === undefined || typeof callback !== 'function' ||
            isDomElem(elem) === false) {
        return;
    }

    let timer;

    // Modified from https://css-tricks.com/snippets/jquery/done-resizing-event/
    // On element resize, clear any existing timeout for the timer var, create
    // a new timeout for the timer var with a delay of a 5th of a second,
    // with callback() as a callback.  The callback will therefore
    // only be executed if no element resize event is called within the
    // timeout window.
    let observer = new ResizeObserver(() => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            callback();
        }, 200);
    });

    // Begin observing the element
    observer.observe(elem);
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

/* Adjust toast arrow elems to remain central to relevant nav elems */
function initArrowPositionAdjuster() {

    /* Adjust the right css property of arrow elems to keep them centralised */
    /* against their respective nav item icons */
    const adjustArrow = (type) => {
        // Iterate over .basket-arrow elems
        $(`.${type}-arrow`).each((i, elem) => {
            // Get the width of the nearest nav item icon
            let liWidth = $(elem).closest('nav').
                find(`.${type}-item a`).
                    outerWidth();

            let widthAdjust = 0;
            let basketWidth = 0;
            let profileMargin = 0;
            let profileLiWidth = 0;
            // If we are adjusting a profile-arrow
            if (type === 'profile') {
                // Get the width of the nearest basket-item
                basketWidth = $(elem).closest('nav').
                    find('.basket-item').
                        outerWidth();

                // Get the margin-right of the nearest profile-item
                profileMargin = parseInt($(elem).closest('nav').
                    find('.profile-item').
                        css('margin-right'));

                // If profileMargin is NaN, set it to 0
                if (profileMargin === 'NaN') {
                    profileMargin = 0;
                }

                // Get the width of the nearest profile-item
                profileLiWidth = $(elem).closest('nav').
                    find(`.${type}-item`).
                        outerWidth();

                // If the profile-item width is greater than the profile-item
                // icon width, use the profile-item width instead
                if (profileLiWidth > liWidth) {
                    liWidth = profileLiWidth;
                }

                // Otherwise further adjust the width by the sum of the
                // basket-item width + profile right margin
                widthAdjust = (basketWidth + profileMargin);
            }

            // If the width is 0, the icon is hidden, so don't bother updating
            if (liWidth > 0) {
                // Set the right css property of the arrow to align with the
                // center of the icon
                $(elem).css('right', (liWidth / 2) + widthAdjust).
                    css('transform', 'translateX(50%)');
            }
        });
    };

    /* Adjust all arrow positions */
    const adjustArrows = () => {
        adjustArrow('basket');
        adjustArrow('profile');
    };

    adjustArrows();

    // Add a resize listener to the window with adjustBasketArrow() as callback
    createResizeListener(adjustArrows);
}

/* Add click listener to Back to Top button */
function initBackToTopButton() {

    // Show the btt button
    const showBtt = () => {
        // Remove the inline height property from the .btt-row
        $('.btt-row').css('height', '');
        // Show the button
        $('button.btt-button').css('visibility', 'initial').
            css('opacity', '1');
    };

    // Hide the btt button
    const hideBtt = () => {
        // Hide the button
        $('button.btt-button').css('visibility', 'hidden').
            css('opacity', '0');
        // Wait .5s for the opacity and visibility button transitions to
        // complete, then set the row height to 0
        setTimeout(() => {
            $('.btt-row').css('height', '0');
        }, 500);
    };

    // Initialise an intersection observer to show/hide the btt button based on
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

    // Adjust toast arrows inline with relevant nav width
    initArrowPositionAdjuster();

    // When a nav element is clicked, hide any toasts
    let navSelector = 'nav a, nav input, nav button, .btt-button';
    $(navSelector).on('click', () => {
        $('.toast').each((i, elem) => {
            bootstrap.Toast.getInstance(elem).hide();
        });
    });
}

function initHeaderSpacer() {
    const adjustSpacer = () => {
        // Update the height of the --adjust-for-header css var inline with the
        // height of the header (including padding/margins)
        $(':root').css('--adjust-for-header', $('header').outerHeight() + 'px');
    };

    // Create a resize observer for the header, and adjust the spacer to match
    createResizeObserver($('header')[0], adjustSpacer);
}

/* doc ready function */
$(() => {
    // Ensure any disabled links do not function
    disableLinks();

    // Add event listeners to search/page input box containers
    initInputBoxShadows();

    // Initialise the Back to Top buttons
    initBackToTopButton();

    // Set product card heights, and create resize listener to call again
    initProductCardHeightAdjust();

    // Initialise Toasts
    initToasts();

    // Initialise header-spacer resize adjustment
    initHeaderSpacer();
});