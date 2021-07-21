# ...................................................Modified Boutique-Ado Code
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # exclude = ('user',)
        fields = (
            'default_phone_number',
            'default_street_address1',
            'default_street_address2',
            'default_town_or_city',
            'default_county',
            'default_postcode',
            'default_country'
        )

    def __init__(self, *args, **kwargs):
        """
            Add placeholders and classes, and remove auto-generated labels
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_county': 'County, State or Locality',
            'default_postcode': 'Postal Code'
        }

        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

            classes_str = 'border-dark stripe-style-input'
            self.fields[field].widget.attrs['class'] = classes_str
            self.fields[field].label = False

            if field == 'default_postcode':
                self.fields[field].widget.attrs['class'] += ' postcode-input'
# ...............................................End Modified Boutique-Ado Code


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
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
            'email': 'Email Address'
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            placeholder = f'{placeholders[field]} *'
            self.fields[field].widget.attrs['placeholder'] = placeholder

            classes_str = 'border-dark stripe-style-input'
            self.fields[field].widget.attrs['class'] = classes_str
            self.fields[field].widget.attrs['required'] = True
            self.fields[field].label = False
