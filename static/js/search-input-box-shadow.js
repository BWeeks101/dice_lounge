/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/

// Document Ready Function
$(function() {
    $('.search-input-container input').on('focus', (e) => {
        $(e.currentTarget).closest('.search-input-container').
            addClass('search-input-container-box-shadow');
    });

    $('.search-input-container input').on('focusout', (e) => {
        $(e.currentTarget).closest('.search-input-container').
            removeClass('search-input-container-box-shadow');
    });

    $('.search-input-container button').on('click', (e) => {
        $(e.currentTarget).closest('.search-input-container').
            addClass('search-input-container-box-shadow');
    });
});