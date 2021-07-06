from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.shortcuts import get_object_or_404


# Custom Validators here.
def validate_whitespace(value):
    if " " in value:
        raise ValidationError('No Spaces Allowed')
    else:
        return value


# Create your models here.
# From boutique ado sample project
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
        help_text='Please enter a descriptive name for this Category.'
    )

    def __str__(self):
        return self.name

    def get_id(self):
        return self.identifier


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
        help_text='Please enter a descriptive name for this Genre.'
    )

    def __str__(self):
        return self.name

    def get_id(self):
        return self.identifier


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
        help_text='Please enter a descriptive name for this Publisher.'
    )

    def __str__(self):
        return self.name

    def get_id(self):
        return self.identifier


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
        help_text='Please enter a descriptive name for this Stock State.'
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
            'Please enter a descriptive name for this Reduced Price Reason.'
        )
    )

    def __str__(self):
        return self.reason

    def get_id(self):
        return self.identifier


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
            'Please enter a descriptive name for this Product Line.'
        )
    )
    category = models.ForeignKey(
        'Category',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text='Please select a category for this Product Line.'
    )
    genre = models.ForeignKey(
        'Genre',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
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
        help_text='Please enter a description for this Product Line.'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        help_text=(
            '(Optional) Please add an image for this Product Line.'
        )
    )

    def __str__(self):
        return self.name

    def get_id(self):
        return self.identifier


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
        help_text=(
            '(Optional) Please add an image for this Sub Product Line.'
        )
    )

    def __str__(self):
        return self.name + ' | ' + str(self.product_line)

    def get_id(self):
        return self.identifier


class Product(models.Model):
    sub_product_line = models.ForeignKey(
        'sub_product_line',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name='Sub-Product Line',
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
        blank=True,
        help_text='Please enter a description for this Product.'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        help_text=(
            '(Optional) Please add an image for this Product.'
        )
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
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
    reduced_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        verbose_name='Reduction %',
        help_text='Please enter the % to reduce the price by.'
    )
    reduced_reason = models.ForeignKey(
        'Reduced_Reason',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Reason for Reduction',
        help_text='Why is this product reduced?'
    )
    stock_state = models.ForeignKey(
        'Stock_State',
        null=True,
        blank=False,
        default=2,
        on_delete=models.SET_NULL,
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
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=False,
        blank=False,
        default=10,
        verbose_name='Max Units Per Purchase',
        help_text='Please enter the max number of units (1-10) available to ' +
        'a single purchase'
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

    # Ensure price reduction reason is set to on_sale if reduction is True
    # (do not enforce reduction value)
    # Ensure stock states are adjusted in line with stock value
    def save(self, *args, **kwargs):
        on_sale = get_object_or_404(Reduced_Reason, identifier='on_sale')
        if self.reduced is True and self.reduced_reason is None:
            self.reduced_reason = on_sale
        elif self.reduced is False:
            self.reduced_reason = None

        in_stock = get_object_or_404(Stock_State, identifier='in_stock')
        out_of_stock = get_object_or_404(
            Stock_State, identifier='out_of_stock')
        unavailable = Stock_State.objects.filter(available=False)
        if self.stock < 1 and self.stock_state == in_stock:
            self.stock_state = out_of_stock
        elif self.stock > 0 and self.stock_state in unavailable:
            self.stock_state = in_stock
        super(Product, self).save(*args, **kwargs)
