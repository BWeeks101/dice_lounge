# The Dice Lounge

### Full Stack Frameworks with Django Milestone Project

All testing was conducted manually, making extensive use of Dev Tools within Mozilla Firefox, Google Chrome and Microsoft Edge.

## Functionality Testing
* Tested with:
    - Browser Dev Tools (Chrome, Firefox, Edge)
    - Galaxy S8 (Chrome, Firefox Mobile)
    - Galaxy S10/S10e (Chrome, Firefox Mobile)
    - 1080p Screens (Chrome, Firefox, Edge)
    - 4k Screens (Chrome, Firefox, Edge)


1. Fully responsive design allows for a functional site on mobile, tablet, laptop and desktop, with a minimum width 280px.
    * The minimum supported width is 280px.  Below this, content will scroll horizontally.
    * The site is fully responsive at all resolutions I have personally tested (280px > 4096px).
    * The site is compatible with the following browsers:
        - Chrome
        - Firefox
        - Edge
    * The site is has been tested and is compatible with the following mobile browsers:
        - Chrome
        - Firefox

    * Safari has not been tested, but should be functional.

    > Meets Website Owner requirement

2. A search field is available at the top of very page to improve product navigation.
    * The search field is at the center of the top navigation bar on desktop, and the nav is fixed at the top of the page.
    * On mobile resolutions the search field is similarly positioned but collapsed, and can be accessed by clicking on an obvious search icon (also on the top nav).
    * Any search for a missing search term will reload the current page (with all URL params intact) and display a clear message regarding the lack of search term.
    * Any search returning o results will reload teh current page (with all URL params intact) and display a clear message regarding the lack of search results.
    * Successful searches will load the search results page and display results, along with many filtering options (displayed in a side bar on desktop and an obvious collapsible sidenav on mobile)
    * Search does not require authentication
    * The search term is displayed at the top of the filter menu.
    * Results are paginated.  The number of displayed results/total results are displayed near the top of the results by the pagination controls.

    > Meets New User Goal 1

    > Meets Shopper Stories 1, 8, 9

3. Users can signup from the Nav menu on every page to create an account and store their order history.
    * The sticky top nav provides access to the registration link on every page

    > Meets New User Goal 2

    > Meets Returning User Story 1

4. Users can navigate to a booking page, allowing them to check availability of tables and complete a booking.
    * Not yet implemented.

5. Returning users may log in to their account, and view their order history from the Profile page.
    * The Profile page is accessible from the top nav on every page.
    * The Profile page displays the users order history, and each order can be selected to display the order confirmation (containing a full breakdown of the order contents, pricing, and delivery details).

    > Meets Returning User Goal 1

6. Returning users may log in to their account and update their stored contact and address information from the Profile page.
    * The Profile page is accessible from the top nav on every page.
    * The Profile page displays standard contact information inputs (first/last name, email, phone) and address inputs.  The inputs show the current stored values for the user (if any).  The user can make changes by directly editing the input values and clicking the update button

    > Meets Returning User Goal 2

7. Store Owners may access the Product Management page when logged in to add new Products.
    * The link to the Product Management page is accessible from the top nav on every page.
    * The link is only available to users logged in with a staff account
    * From this page, New product lines, sub product lines, products, categories, genres, publishers, reduction reasons and stock states may all be added.
    * Existing entities of the same types may also be located, selected and edited (including applying/removing price reductions, and setting stock levels).
    * Product lines, sub product lines and products may be hidden (effectively removed from the site entirely), or restored.

    > Meets Store Owner Stories, 1, 2, 3 and 4

8. When logged in, Store Owners may click the 'Edit' button on any Product to directly edit the Product details, set it's availability, and add/remove price reductions.
    * Edit buttons are available on product cards on the All Games, Products, Product Detail and Search Result pages.
    * Edit buttons are only available to users logged in with a staff account
    * Clicking an edit button will open the Edit page for that product.

    > Meets Store Owner Stories 2, 3 and 4

9. Shoppers may perform a search or view products via the navigation menus to select some to purchase.
    * Search is available from every page via the input situated in the top nav.
    * The product navigation menus are available on every page either in the top nav or the main sidenav (accessed via the burger button in the top left corner)

    > Meets New User Goal 1

    > Meets Shopper Stories 1, 3, 8

10. Shoppers may click on any item to see a more detailed view in the Product Detail page.
    * Shoppers may click on a product image on the Products, Search Results and Basket views to be taken to the Product Detail page for that product.

    > Meets Shopper Story 2

11. When searching for items, Shoppers can apply filters to the results, including filtering for products that are reduced in price.
    * When viewing search results, users have filters available on the sidebar/sidenav.  The available filters are always specific to the returned results (ie, if there are no On Sale products, there will be no filter for On Sale products).  Multiple filters can be applied simultaneously.

    > Meets Shopper Stories 1, 3, 5, 6, 7, 8

12. Shoppers can see their basket total below the basket icon on the sticky navigation bar at the top of the page.
    * The total is clearly visible below the basket icon on the top nav on all pages

    > Meets Shopper Story 4

13. Shoppers can sort Product Lists and Search Results by a number of criteria, including name and price.
    * When viewing products/search results, multiple filters can be applied via the the sidebar/sidenav.

    > Meets Shopper Stories 5, 6, 7

14. Shoppers can apply multiple filters simultaneously to any given list of products along with a sort criteria.
    * Multiple filters can be applied simultaneously, along with a single sort criteria.

    > Meets Shopper Stories 5, 6, 7

15. Shoppers can enter a search term from the search input on any page, which will target multiple fields, including name, description, product line and sub product line.
    * The search function targets all of these fields in an effort to provide as many relevant results as possible.

    > Meets Shopper Stories 1, 8

16. When search results are returned, the search term and number of results are shown at the top of the page, above the list of products that were located.
    * The All Games, Products and Search Results pages are paginated.  The the total number of displayed records is visible next to the total number of returned records.

    > Meets Shopper Story 9

17. Shoppers may add items to their basket from the Detail page for that product.  The page features a quantity input, allowing the user to select how many of the item they wish to add.
    * The product detail page features a dropdown to select the quantity required, and an add to basket button.
    * The Products and Search Results views display an Add to Basket button over each product.  When clicked this button will add a single instance of the item to the users basket.

    > Meets Shopper Stories 2, 10,

18. Shoppers may view the contents of their basket by clicking the basket icon at the top of any page.  The basket page shows the list of items in the basket (including a small image and some basic details), the quantity of that item, and the subtotal of those items.  Quantity controls are displayed to adjust the number of any given item.  A 'remove' link is also present should the Shopper wish to remove all instances of a Product from their basket.
    * The basket icon is available in the top nav on every page.
    * The basket page shows all items in the basket, along with price, quantity and sub total for each item.
    * A remove link is present for each item.

    > Meets Shopper Stories 11, 12

19. The checkout features a simple form for entering required contact, billing and card information.
    * The checkout form is very straight forward, providing only standard fields.  No inside-leg measurement required!
    * The checkout form will be prepopulated (except for the credit card input) should the user be logged in and have saved details on their profile.

    > Meets Shopper Story 13, 14

20. Card details are never stored.  Contact and Address information is secured behind an account system.  Secure Payment information is handled by Stripe.
    * The site has no facility to store card details.
    * Secure payments are handled by Stripe.
    * All profile information is secured behind django's account system, enhanced by allauth.

    > Meets Shopper Story 14

21. Once an order is complete, the Shopper is redirected to an Order Confirmation page which displays an order summary featuring product, contact and delivery information.
    * Fully functional.  The user is automatically shown the Order Confirmation, which includes the order summary.

    > Meets Shopper Story 15

22. When an order is completed, an email is sent to the Shopper at the email address they provided, containing an order summary.
    * Fully functional.  The user will automatically receive an emailed order summary at the provided address when an order completes.

    > Meets Shopper Story 16

23. Returning users may log in/out from the Account menu at the top of every page.
    * The sign in/out functionality is available on the top nav on every page.

    > Meets Returning User Story 2

24. Returning users may recover their password from the 'Forgot Password?' link on the login page
    * If a user cannot remember their password, they are free to use the Forgot Password link on the sign in page.
    * Alternatively they can email support and a staff member can reset the password via the built in Django Admin.

    > Meets Returning User Story 3

25. As part of the registration process, a user will receive an email containing a confirmation link.  Clicking this link will complete the registration process and advise the user that it was successful.
    * When signing up the user must provide an email address
    * A confirmation link will be sent to that address
    * The user cannot sign into their account until they have followed the link and clicked to confirm account creation.
    * As soon as the user clicks to confirm, they will receive a message confirming the creation of their account.

    > Meets User Story 4

26. When completing a table booking, users will receive a booking confirmation via email.
    * Not implemented.

*All user/administrator actions are authenticated defensively by the server application.  Unauthorised requests are handled, denied and/or redirected*