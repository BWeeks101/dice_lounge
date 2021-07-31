from django import forms
from django.conf import settings
from .widgets import CustomClearableFileInput
from .models import (
    Category, Genre, Product_Line, Publisher, Reduced_Reason, Stock_State,
    Product, Sub_Product_Line
)


# Helper function for setting active field
def setFocus(field):
    field.widget.attrs['autofocus'] = True


# Shortcut function for setting form control styling
def setStyling(fields, placeholders):
    for field in fields:
        field_type = str(type(fields[field]).__name__).lower()

        if fields[field].required:
            placeholder = f'{placeholders[field]} *'
            fields[field].widget.attrs['required'] = True
        else:
            placeholder = placeholders[field]
        if field_type != 'booleanfield':
            fields[field].label = False
            if field_type != 'imagefield':
                fields[field].widget.attrs['placeholder'] = placeholder
                fields[field].widget.attrs['class'] = 'stripe-style-input'

        if field_type != 'imagefield' and field_type != 'booleanfield':
            classes_str = ' border-dark'
            fields[field].widget.attrs['class'] += classes_str


class Category_Form(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'identifier': 'Identifier',
            'name': 'Category Name'
        }

        setFocus(self.fields['identifier'])

        setStyling(self.fields, placeholders)


class Genre_Form(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'identifier': 'Identifier',
            'name': 'Genre Name'
        }

        setFocus(self.fields['identifier'])

        setStyling(self.fields, placeholders)


class Publisher_Form(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'identifier': 'Identifier',
            'name': 'Publisher Name'
        }

        setFocus(self.fields['identifier'])

        setStyling(self.fields, placeholders)


class Stock_State_Form(forms.ModelForm):
    class Meta:
        model = Stock_State
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'identifier': 'Identifier',
            'state': 'Stock State',
            'available': 'Available to Order?'  # boolean.  revise styling?
        }

        setFocus(self.fields['identifier'])

        setStyling(self.fields, placeholders)


class Reduced_Reason_Form(forms.ModelForm):
    class Meta:
        model = Reduced_Reason
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'identifier': 'Identifier',
            'reason': 'Reason for Reduction?',
            'default_reduction_percentage': 'Please set a default reduction ' +
            'percentage for this Reduction Reason'
        }

        self.fields['default_reduction_percentage'].widget.attrs['min'] = 0
        self.fields['default_reduction_percentage'].widget.attrs['max'] = (
            settings.MAX_PERCENTAGE_REDUCTION)

        setFocus(self.fields['identifier'])

        setStyling(self.fields, placeholders)


class Product_Line_Form(forms.ModelForm):
    class Meta:
        model = Product_Line
        fields = '__all__'

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = (
            [(
                category.id, category
             ) for category in Category.objects.all()
             ]
        )
        genres = (
            [(
                genre.id, genre.name
             ) for genre in Genre.objects.all()
             ]
        )
        publishers = (
            [(
                publisher.id, publisher
             ) for publisher in Publisher.objects.all()
             ]
        )

        placeholders = {
            'identifier': 'Identifier',
            'name': 'Product Line Name',
            'category': 'Select a Category',  # Dropdown
            'genre': 'Select a Genre',  # Dropdown
            'publisher': 'Select a Publisher',  # Dropdown
            'description': 'Enter a description',  # Not required
            # Image input, Not required
            'image': 'Please add an image for this Product Line',
            'hidden': 'Should this Product Line be hidden?'
        }

        self.fields['category'].choices = categories
        self.fields['genre'].choices = genres
        self.fields['publisher'].choices = publishers

        setFocus(self.fields['identifier'])

        setStyling(self.fields, placeholders)


class Sub_Product_Line_Form(forms.ModelForm):
    class Meta:
        model = Sub_Product_Line
        fields = '__all__'

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'product_line': 'Select a Product Line',  # Dropdown
            'identifier': 'Identifier',
            'name': 'Sub Product Line Name',
            'description': 'Enter a description',  # Not required
            # Boolean
            'core_set': 'Does this Sub Product Line contain Core Sets/Rules?',
            # Boolean
            'scenics': 'Does this Sub Product Line contain Scenics and/or \
                Terrain?',
            # Image input, Not required
            'image': 'Please add an image for this Sub Product Line',
            'hidden': 'Should this Sub Product Line be hidden?'
        }

        setFocus(self.fields['product_line'])

        setStyling(self.fields, placeholders)


class Product_Form(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'sub_product_line',
            'identifier',
            'name',
            'description',
            'image',
            'price',
            'reduced',
            'reduced_reason',
            'reduced_percentage',
            'stock_state',
            'stock',
            'max_per_purchase',
            'hidden'
        )

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sub_product_lines = (
            [(
                sub.id, sub
             ) for sub in Sub_Product_Line.objects.all()
             ]
        )
        reduced_reasons = (
            [(rr.id, rr.reason) for rr in Reduced_Reason.objects.all()]
        )
        stock_states = (
            [(state.id, state.state) for state in Stock_State.objects.all()]
        )

        placeholders = {
            'sub_product_line': 'Select a Sub Product Line',  # Dropdown
            'identifier': 'Identifier',
            'name': 'Product Name',
            'description': 'Enter a description',  # Not required
            # Boolean
            # Image input, Not required
            'image': 'Please add an image for this Sub Product Line',
            'price': 'Enter the price (GBP)',
            # Boolean
            'reduced': 'Is the price of this item reduced?',
            'reduced_reason': 'Select a reason for the reduction',  # Dropdown
            'reduced_percentage': 'Enter the % to reduce by',
            'stock_state': 'Select a stock state for this product',  # Dropdown
            'stock': 'Number of units in stock',
            # Dropdown
            'max_per_purchase': 'Max number of units per transaction (1-10)',
            'hidden': 'Should this Product be hidden?'
        }

        self.fields['sub_product_line'].choices = sub_product_lines
        self.fields['reduced_reason'].choices = reduced_reasons
        self.fields['reduced_percentage'].widget.attrs['min'] = 0
        self.fields['reduced_percentage'].widget.attrs['max'] = (
            settings.MAX_PERCENTAGE_REDUCTION
        )
        self.fields['stock_state'].choices = stock_states
        self.fields['max_per_purchase'].widget.attrs['min'] = 1
        self.fields['max_per_purchase'].widget.attrs['max'] = (
            settings.DEFAULT_MAX_PER_PURCHASE
        )

        setFocus(self.fields['sub_product_line'])

        setStyling(self.fields, placeholders)

        def get_sub_product_line_id(self, name):
            for sub in sub_product_lines:
                if sub.name == name:
                    return sub.id

            return None
