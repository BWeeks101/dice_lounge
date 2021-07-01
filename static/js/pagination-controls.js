/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/

/* Add click listener to pagination controls */
function initPaginationControls() {
    // Load the specified page
    const loadPage = (page) => {
        // Get the current url
        let currentUrl = new URL(window.location);

        // If page is undefined, return
        if (page === undefined) {
            return;
        }

        // Update the page number in the url
        currentUrl.searchParams.set('page', page);

        // Load the updated url
        window.location.replace(currentUrl);
    };

    // Listen for .page-link click, and load the page
    $('.pagination > .page-item > .page-link').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the target page value
        let page = $(e.currentTarget).attr('data-page');

        // Load the page
        loadPage(page);
    });

    // Listen for enter keypress in .page-input, and load the page
    $('.page-input').on('keyup', (e) => {
        // If Enter was pressed
        if (e.keyCode === 13) {
            // Get the input value
            let page = $(e.currentTarget).val();

            // Load the page
            loadPage(page);
        }
    });

    /* Add click listeners to dropdown items to apply sort */
    $('.pagination-dropdown .dropdown-item').on('click', (e) => {
        // prevent the default link click action
        e.preventDefault();

        // Get the current url
        let currentUrl = new URL(window.location);

        // Get the sort value
        let selectedVal = $(e.currentTarget).attr('data-value');

        // Update the url
        currentUrl.searchParams.set('numprod', selectedVal);

        // Reset the results to page 1
        currentUrl.searchParams.delete('page');

        // Load the updated url
        window.location.replace(currentUrl);
    });
}

$(function() {
    initPaginationControls();
});