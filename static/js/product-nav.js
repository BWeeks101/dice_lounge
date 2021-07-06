/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global initCollapsibleTogglerArrows */

/* Restyle sideNav menu dropdowns to collapsibles and add click */
/* listeners */
function offCanvasDropdownToCollapse() {
    let selector = `#sideNav .product-nav-ul li.dropdown > ` +
        `a[id][data-bs-toggle=dropdown]`;
    let togglers = $(selector);
    if (togglers.length > 0) {
        $(togglers).each((i, toggler) => {
            // Update the toggler
            $(toggler).attr('id', `sideNav-${$(toggler).attr('id')}`).
                attr('data-bs-toggle', 'collapse').
                    attr('data-bs-target',
                        `#${$(toggler).attr('id')}-collapsible`).
                            removeClass('show');

            // Update the dropdown-menu
            $(toggler).next().
                attr('id', `${$(toggler).attr('id')}-collapsible`).
                    attr('aria-labelledby',
                        `${$(toggler).attr('id')}`).
                            addClass('collapse').
                                removeClass('dropdown-menu').
                                    removeClass('border').
                                        removeClass('border-dark').
                                            removeClass('shadow-lg').
                                                removeClass('show');

            /* Invert arrow on toggler when clicked */
            initCollapsibleTogglerArrows(toggler);
        });

        // Add active class to selected product filter on .product-navbar
        // and #sideNav

        // Get .product-navbar dropdown-items
        let itemSelector = '.product-navbar .product-nav-ul ' +
            'li.dropdown > a[id] ~ .dropdown-menu > .dropdown-item';
        let dropDownItems = $(itemSelector);

        // Get #sideNav dropdown-items
        let sideNavItemSelector = '#sideNav .product-nav-ul ' +
            'li.dropdown > a[id] ~ .collapse > .dropdown-item';
        let sideNavCollapseItems = $(sideNavItemSelector);

        /* Remove the .active class from product-nav and #sideNav */
        /* .dropdown-items */
        const removeActiveClass = () => {
            $(itemSelector + '.active, ' + sideNavItemSelector + '.active').
                removeClass('active');
        };

        /* Add the .active class to a pair of product-nav .dropdown-items */
        const addActiveClass = (i) => {
            removeActiveClass();
            $(dropDownItems[i]).addClass('active');
            $(sideNavCollapseItems[i]).addClass('active');
        };

        /* On .product-navbar dropdown-item click, apply active class to */
        /* .product-navbar dropdown-item, and paired #sideNav */
        /* dropdown-item */
        $(dropDownItems).each((i, item) => {
            $(item).on('click', () => {
                addActiveClass(i);
            });
        });

        /* On #sideNav dropdown-item click, apply active class to */
        /* #sideNav dropdown-item, and paired .product-navbar */
        /* dropdown-item */
        $(sideNavCollapseItems).each((i, sideNavItem) => {
            $(sideNavItem).on('click', () => {
                addActiveClass(i);
            });
        });
    }
}

/* doc ready function */
$(() => {
    // Restyle sideNav menu dropdowns to collapsibles and add listeners
    offCanvasDropdownToCollapse();
});