/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global isDomElem */

/* Ensure the clicked element was a list-group-item */
function isListClickValid(elem) {
    if (!isDomElem(elem)) {
        return false;
    }
    if (!$(elem).hasClass('list-group-item')) {
        if (!$(elem).closest('list-group-item').length > 0) {
            return false;
        }
    }
    return true;
}

/* Disable a List */
/* Requires: */
/*  listElem: Object.  List element */
function disableList(listElem) {
    // Disable the list items
    $(listElem).find('.list-group-item').
        attr('disabled', true).
            addClass('pe-none');
}

/* Get the disabled state of a list */
/* Requires: */
/*  listElem: Object.  List element */
/* NB: Will return true is *any* list items are disabled.  Not an issue for */
/* this implementation, but worth bearing in mind. */
// eslint-disable-next-line no-unused-vars
function getListDisabledState(listElem) {
    let selector = '.list-group-item[disabled=true], ' +
        '.list-group-item[disabled=disabled]';
    let items = !$(listElem).find(selector);
    return items;
}

/* Set list loading message */
/* Requires: */
/*  listElem: Object.  List element */
function setListLoadingMessage(listElem) {
    $(listElem).html(
                `<div class="list-group-item list-group-item-action>
                    <span class="text-dark">Loading...</span>
                    <span class="text-dark icon">
                        <i class="fas fa-sync-alt fa-spin"></i>
                    </span>
                </div>`
            );
}

/* Set dropdown loading error message */
/* Requires: */
/*  ListElem: Object.  List element. */
/* Optional: */
/*  toggleMessage: String.  Text to display in the toggler */
/*  errorMessage: String.  Text to display in the error message */
function setListErrorMessage(listElem, toggleMessage, errorMessage) {
    if (!toggleMessage) {
        toggleMessage = 'An error occurred...';
    }
    if (!errorMessage) {
        errorMessage = 'Unable to retrieve list data from the server.  ' +
            'Please reload the page and try again.';
    }
    $(listElem).html(
                `<div class="list-group-item list-group-item-action">
                    <span class="text-danger icon">
                        <i class="fas fa-exclamation"></i>
                    </span>
                    <span class="text-danger">${toggleMessage}</span>
                </div>`
            );
    $(listElem).closest('.list-wrapper').
        find('.list-error-message').
            html(`<span class="small text-danger">${errorMessage}</span>`).
                removeClass('d-none');
    $(listElem).closest('.list-wrapper').
        find('.list-help-text').
            addClass('d-none');
}

/* Clear dropdown loading error message */
/* Requires: */
/*  listElem: Object.  List element */
function clearListErrorMessage(listElem) {
    $(listElem).html('');
    $(listElem).closest('.list-wrapper').
        find('.list-error-message').
            html('').
                addClass('d-none');
    $(listElem).closest('.list-wrapper').
        find('.list-help-text').
            removeClass('d-none');
}

/* Display error message on post failure or error */
/* Requires: */
/*  listElem: Object.  List element */
/* Optional: */
/*  toggleMessage: String.  Text to display in the toggler */
/*  errorMessage: String.  Text to display in the error message */
function popListFailure(listElem, toggleMessage, errorMessage) {
    setListErrorMessage($(listElem), toggleMessage, errorMessage);
    disableList($(listElem));
}

/* Populate a list using data returned from a server request */
/* Requires: */
/*  response: Response data from the server */
/*  listElem: Object.  List element */
/*  callback: Function.  Callback function to execute post completion */
function popList(response, listElem, callback) {
    // Clear any existing list error message content
    clearListErrorMessage($(listElem));

    // If the response returned no objects, display the default error, fire the
    // callback and return
    if (response.length < 1) {
        popListFailure($(listElem));
        if (typeof callback === 'function') {
            return callback();
        }
        return;
    }

    // Iterate over the response
    response.forEach((obj, i) => {
        // generate the dropdown-item elem html
        let item = '<button href="#!" class="list-group-item ' +
            'list-group-item-action hover-background-red" data-value="' +
            `${response[i].id}">`;

        let itemText = response[i].name;
        if (response[i].hidden && response[i].hidden === true) {
            itemText += '<span class="icon icon-red"><i class="fas fa-ghost">' +
                '</i></span>';
        }
        item += `${itemText}</button>`;

        // add the dropdown as a new child of the menu element
        $(listElem).append(item);
    });

    // If we got a single response with an id of -1, there was an issue
    // returning a valid list from the server
    if (response.length === 1 && response[0].id === '-1') {
        popListFailure(
            $(listElem),
            response[0].name,
            response[0].error
        );
    }

    // Fire the callback, passing response as a parameter
    if (typeof callback === 'function') {
        return callback(response);
    }
}

/* Submit a post request to get data with which to populate a list */
/* Requires: */
/*  listElem: Object.  List that will display the lookup data */
/*  lookupType: String.  Table to interrogate. */
/* Optional: */
/*  extraData: Object.  Additional key:value pairs to add to the post request */
/*  callback: Function.  Callback function to execute post completion */
// eslint-disable-next-line no-unused-vars
function submitListRequest({listElem, lookupType, extraData, callback}) {
    // if listElem does not exist in the dom, return
    if (!isDomElem(listElem)) {
        return;
    }

    // If lookupType is not a string, return
    if (typeof lookupType !== 'string' || lookupType.length < 1) {
        return;
    }

    // set the loading message in the list
    setListLoadingMessage($(listElem));

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
        // If we get a response, populate the list
        popList(response, $(listElem), callback);
    }).fail(() => {
        // If the post request fails, display an error
        popListFailure($(listElem));
        if (typeof callback === 'function') {
            return callback();
        }
    });
}

function initProductList() {
    if (!isDomElem($('#productList'))) {
        return;
    }

    // Add click listener to list to catch clicks on list-group-item elements
    $('#productList').on('click', (e) => {
        // Prevent the default action
        e.preventDefault();

        // If a list-group-item (or descendent of) was not the click
        // target, return
        if (!isListClickValid($(e.target))) {
            return;
        }

        $('#productList .list-group-item.active').removeClass('active');
        $(e.target).addClass('active');
    });
}

$(() => {
    initProductList();
});