from django.core.exceptions import ValidationError
from django.core.validators import (
    DecimalValidator, MinValueValidator, MaxValueValidator)
from django.db import models
from django.shortcuts import get_object_or_404
from django.conf import settings
from decimal import Decimal


# Custom Validators here.
# Prevent whitespace from being included in a field
def validate_whitespace(value):
    if " " in value:
        raise ValidationError('No Spaces Allowed')
    else:
        return value


# Create your models here.
# Product Line images written to:
#   <media root>/covers/<publisher.identifier>/
def product_line_image_path(instance, filename):
    return f'covers/{instance.publisher.identifier}/{filename}'


# Sub Product Line images written to:
#   <media root>/<product_line.identifier>/
def sub_product_line_image_path(instance, filename):
    return f'{instance.product_line.identifier}/{filename}'


# Product images written to:
#   <media root>/<product_line.identifier>/<sub_product_line.identifier>
def product_image_path(instance, filename):
    return (f'{instance.sub_product_line.product_line.identifier}/' +
            f'{instance.sub_product_line.identifier}/{filename}')


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    identifier = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_whitespace],
        verbose_name='Category Identifier',
        help_text='Please use underscores instead of spaces.  Must be unique.'
    )
    name = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Category',
        help_text='Please enter a descriptive name for this Category.  \
            Must be unique.'
    )

    def __str__(self):
        return self.name

    def get_id(self):
        return self.identifier

    def clean(self):
        self.identifier = self.identifier.lower()


class Genre(models.Model):
    identifier = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_whitespace],
        verbose_name='Genre Identifier',
        help_text='Please use underscores instead of spaces.  Must be unique.'
    )
    name = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Genre',
        help_text='Please enter a descriptive name for this Genre.  \
            Must be unique.'
    )

    def __str__(self):
        return self.name

    def get_id(self):
        return self.identifier

    def clean(self):
        self.identifier = self.identifier.lower()


class Publisher(models.Model):
    identifier = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_whitespace],
        verbose_name='Publisher Identifier',
        help_text='Please use underscores instead of spaces.  Must be unique.'
    )
    name = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Publisher',
        help_text='Please enter a descriptive name for this Publisher.  \
            Must be unique.'
    )

    def __str__(self):
        return self.name

    def get_id(self):
        return self.identifier

    def clean(self):
        self.identifier = self.identifier.lower()


class Stock_State(models.Model):
    class Meta:
        verbose_name = "Stock State"

    identifier = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_whitespace],
        verbose_name='Stock State Identifier',
        help_text='Please use underscores instead of spaces.  Must be unique.'
    )
    state = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Stock State',
        help_text='Please enter a descriptive name for this Stock State.  \
            Must be unique.'
    )
    available = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        verbose_name='Available to Order?',
        help_text='Does this Stock State indicate that items are available ' +
        'to order?'
    )

    def __str__(self):
        return self.state

    def get_id(self):
        return self.identifier

    def clean(self):
        self.identifier = self.identifier.lower()


class Reduced_Reason(models.Model):
    class Meta:
        verbose_name = "Reduced Price Reason"

    identifier = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_whitespace],
        verbose_name='Reduced Price Reason Identifier',
        help_text='Please use underscores instead of spaces.  Must be unique.'
    )
    reason = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Reduced Price Reason',
        help_text=(
            'Please enter a descriptive name for this Reduced Price Reason.  \
                Must be unique.'
        )
    )
    default_reduction_percentage = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(settings.MAX_PERCENTAGE_REDUCTION)
        ],
        null=False,
        blank=False,
        default=settings.DEFAULT_PERCENTAGE_REDUCTION,
        verbose_name='Default Price Reduction Percentage',
        help_text='Please enter a default reduction % for this ' +
        f'reason (0-{settings.MAX_PERCENTAGE_REDUCTION}).'
    )

    def __str__(self):
        return self.reason

    def get_id(self):
        return self.identifier

    def clean(self):
        self.identifier = self.identifier.lower()


class Product_Line(models.Model):
    class Meta:
        verbose_name = "Product Line"

    identifier = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_whitespace],
        verbose_name='Product Line Identifier',
        help_text='Please use underscores instead of spaces.  Must be unique.'
    )
    name = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Product Line',
        help_text=(
            'Please enter a descriptive name for this Product Line.  \
                Must be unique.'
        )
    )
    category = models.ForeignKey(
        'Category',
        null=False,
        blank=False,
        on_delete=models.RESTRICT,
        help_text='Please select a category for this Product Line.'
    )
    genre = models.ForeignKey(
        'Genre',
        null=False,
        blank=False,
        on_delete=models.RESTRICT,
        help_text='Please select a genre for this Product Line.'
    )
    publisher = models.ForeignKey(
        'Publisher',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text='Please select a publisher for this Product Line.'
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Please enter a description for this Product Line.'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        max_length=2000,
        upload_to=product_line_image_path,
        help_text=(
            '(Optional) Please add an image for this Product Line.'
        )
    )
    hidden = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        help_text='Hide this Product Line (and all child Sub Product Lines and \
            Products) from view?'
    )

    def __str__(self):
        return self.name

    def get_id(self):
        return self.identifier

    def is_hidden(self):
        return self.hidden

    def clean(self):
        self.identifier = self.identifier.lower()


class Sub_Product_Line(models.Model):
    class Meta:
        verbose_name = "Sub Product Line"

    product_line = models.ForeignKey(
        'Product_Line',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text='Please assign this Sub Product Line to a Product Line'
    )
    identifier = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_whitespace],
        verbose_name='Sub Product Line Identifier',
        help_text='Please use underscores instead of spaces.  Must be unique.'
    )
    name = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        verbose_name='Sub Product Line',
        help_text=(
            'Please enter a descriptive name for this Sub Product Line.'
        )
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Please enter a description for this Sub Product Line'
    )
    core_set = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        help_text='Does this Sub Product Line contain Core Sets/Rules?'
    )
    scenics = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        help_text='Does this Sub Product Line contain Scenics and/or Terrain?'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        max_length=2000,
        upload_to=sub_product_line_image_path,
        help_text=(
            '(Optional) Please add an image for this Sub Product Line.'
        )
    )
    hidden = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        help_text='Hide this Sub Product Line (and all child Products) from \
            view?'
    )

    def __str__(self):
        return self.name + ' | ' + str(self.product_line)

    def get_id(self):
        return self.identifier

    def is_hidden(self):
        return self.hidden

    def clean(self):
        if self.core_set and self.scenics:
            raise ValidationError(
                {
                    'core_set': "Only one of Core Set or Scenics should be \
                    true,not both.",
                    'scenics': "Only one of Core Set or Scenics should be \
                    true,not both."
                })

        self.identifier = self.identifier.lower()


class Product(models.Model):
    sub_product_line = models.ForeignKey(
        'sub_product_line',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name='Sub Product Line',
        help_text='Please assign this Product to a Sub Product Line.'
    )
    identifier = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_whitespace],
        verbose_name='Product Identifier',
        help_text='Please use underscores instead of spaces.  Must be unique.'
    )
    name = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        verbose_name='Product Name',
        help_text=(
            'Please enter a descriptive name for this Product.'
        )
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Please enter a description for this Product.'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        max_length=2000,
        upload_to=product_image_path,
        help_text=(
            '(Optional) Please add an image for this Product.'
        )
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            DecimalValidator(6, 2),
            MinValueValidator(Decimal('0.01'))
        ],
        null=False,
        blank=False,
        default=999.99,
        help_text='Please enter the price of this product (GBP).'
    )
    reduced = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name='Reduced?',
        help_text='Is the price of this item reduced?'
    )
    reduced_reason = models.ForeignKey(
        'Reduced_Reason',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        verbose_name='Reason for Reduction',
        help_text='Why is this product reduced?'
    )
    reduced_percentage = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(settings.MAX_PERCENTAGE_REDUCTION)
        ],
        default=0,
        verbose_name='Reduction %',
        help_text='Please enter the % to reduce the price by (0-' +
        f'{settings.MAX_PERCENTAGE_REDUCTION}).'
    )
    reduced_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            DecimalValidator(6, 2),
            MinValueValidator(Decimal('0.01'))
        ],
        null=False,
        blank=False,
        default=0.00,
        help_text='Auto calculated.  Do not update this field.'
    )
    stock_state = models.ForeignKey(
        'Stock_State',
        null=True,
        blank=False,
        default=2,
        on_delete=models.RESTRICT,
        verbose_name='Stock State',
        help_text='What is the stock status of this product?'
    )
    stock = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=False,
        blank=False,
        default=0,
        verbose_name='Units in Stock',
        help_text='Please enter the number of units of this product in stock.'
    )
    max_per_purchase = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(settings.DEFAULT_MAX_PER_PURCHASE)
        ],
        null=False,
        blank=False,
        default=settings.DEFAULT_MAX_PER_PURCHASE,
        verbose_name='Max Units Per Purchase',
        help_text='Please enter the max number of units ' +
        f'(1-{settings.DEFAULT_MAX_PER_PURCHASE}) available to a single ' +
        'purchase'
    )
    hidden = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        help_text='Hide this Product from view?'
    )

    def __str__(self):
        return self.name

    def get_id(self):
        return self.identifier

    def get_stock(self):
        return {
            'stock_state': self.stock_state,
            'stock': self.stock
        }

    def is_hidden(self):
        return self.hidden

    def clean(self):
        self.identifier = self.identifier.lower()

    # Ensure price reduction reason is set to on_sale if reduction is True and
    # no reason is otherwise selected.  If the reduction percentage is 0, set
    # it to the default percentage reduction for the selected reason
    def save(self, *args, **kwargs):
        if self.reduced is True and self.reduced_reason is None:
            self.reduced_reason = get_object_or_404(
                Reduced_Reason, identifier='on_sale')
        if self.reduced is True and self.reduced_percentage == 0:
            reason = get_object_or_404(
                Reduced_Reason, reason=self.reduced_reason)
            self.reduced_percentage = reason.default_reduction_percentage
        elif self.reduced is False:
            self.reduced_reason = None
            self.reduced_percentage = 0

        if (self.reduced is True and self.reduced_reason and
                self.reduced_percentage > 0):
            self.reduced_price = (
                self.price - ((self.price / 100) * self.reduced_percentage))
        else:
            self.reduced_price = self.price

        # Ensure stock states are adjusted in line with stock value
        in_stock = get_object_or_404(Stock_State, identifier='in_stock')
        out_of_stock = get_object_or_404(
            Stock_State, identifier='out_of_stock')
        unavailable = Stock_State.objects.filter(available=False)
        if self.stock < 1 and self.stock_state == in_stock:
            self.stock_state = out_of_stock
        elif self.stock > 0 and self.stock_state in unavailable:
            self.stock_state = in_stock

        super(Product, self).save(*args, **kwargs)

    def get_price(self):
        # If the price is greater than the reduced price, and the reduced price
        # is 0, call self.save() to ensure the reduced price is updated
        if self.price > self.reduced_price and self.reduced_price == 0.00:
            self.save()
        # Alternatively, if the price is greater than the reduced price, call
        # self.save() to ensure the reduced price is updated
        elif self.price < self.reduced_price:
            self.save()

        # Return the price and the reduced price.
        return {
            'base_price': self.price,
            'price': self.reduced_price
        }
