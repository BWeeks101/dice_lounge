/*eslint func-style: ["error", "declaration", { "allowArrowFunctions": true }]*/
/*global submitPostcode, submitCountry */

/* Add submit listener to profile update form to ensure that the postcode */
/* and country validate prior to submission */
function initUpdateProfileForm() {
    $('#profile-update-form').on('submit', (e) => {
        e.preventDefault();
        // Disable the submit button to prevent multiple clicks
        $(e.currentTarget).find('button').
            attr('disabled', true);

        /* Ensure that the postcode/country are valid before form submission */
        const submitForm = () => {
            // If the postcode/country are not valid, enable the submit button
            // and return
            if ($('input[data-isvalid=false]').length > 0) {
                $(e.currentTarget).find('button').
                    attr('disabled', false);
                return;
            }

            // Otherwise submit the form to update the profile address info
            $('#profile-update-form')[0].submit();
        };

        // Chain submitPostcode->submitCountry->submitForm to ensure the form
        // is not submitted when postcode/country are not valid
        // (Chaining the callbacks ensures each async server call completes
        // before proceeding)
        submitPostcode(
            $('#id_default_postcode'),
            () => submitCountry(
                $('#id_default_country'),
                submitForm
            )
        );
    });
}

/* doc ready function */
$(() => {
    initUpdateProfileForm();
});