# ...................................................Modified Boutique-Ado Code
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'county',
            'postcode',
            'country',
            'delivery_first_name',
            'delivery_last_name',
            'delivery_address1',
            'delivery_address2',
            'delivery_town_or_city',
            'delivery_county',
            'delivery_postcode',
            'delivery_country'
        )

    def __init__(self, *args, **kwargs):
        """
            Add placeholders and classes, remove auto-generated labels and set
            autofocus on first field.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'county': 'County',
            'postcode': 'Post Code',
            'delivery_first_name': 'Recipient First Name',
            'delivery_last_name': 'Recipient Last Name',
            'delivery_address1': 'Street Address 1',
            'delivery_address2': 'Street Address 2',
            'delivery_town_or_city': 'Town or City',
            'delivery_county': 'County',
            'delivery_postcode': 'Post Code'
        }

        # Give focus to the first_name input
        self.fields['first_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            # If the country/delivery country field, set it to required
            if field != 'country' and field != 'delivery_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

            # If we have a delivery input, set it to disabled and give it the
            # d-none class to prevent display
            if field.startswith("delivery_"):
                self.fields[field].widget.attrs['class'] += ' d-none'
                self.fields[field].widget.attrs['disabled'] = True

            if field == 'postcode' or field == 'delivery_postcode':
                self.fields[field].widget.attrs['class'] += ' postcode-input'
# ...............................................End Modified Boutique-Ado Code
