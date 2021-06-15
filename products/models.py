from django.core.exceptions import ValidationError
from django.db import models


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
    image_url = models.URLField(
        max_length=1024,
        null=True,
        blank=True,
        help_text=(
            '(Optional) Please enter an image URL for this Product Line.'
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
    image_url = models.URLField(
        max_length=1024,
        null=True,
        blank=True,
        help_text=(
            '(Optional) Please enter an image URL for this Sub Product Line.'
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
        verbose_name='Product',
        help_text=(
            'Please enter a descriptive name for this Product.'
        )
    )
    description = models.TextField(
        help_text='Please enter a description for this Product.'
    )
    image_url = models.URLField(
        max_length=1024,
        null=True,
        blank=True,
        help_text=(
            '(Optional) Please enter an image URL for this Product.'
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
        help_text='Is the price of this item reduced?'
    )
    reduced_percentage = models.IntegerField(
        help_text='Please enter the % to reduce the price by.'
    )
    reduced_reason = models.ForeignKey(
        'Reduced_Reason',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Why is this product reduced?'
    )
    stock_state = models.ForeignKey(
        'Stock_State',
        null=True,
        blank=True,
        default=2,
        on_delete=models.SET_NULL,
        help_text='What is the stock status of this product?'
    )
    stock = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        help_text='Please enter the number of units of this product in stock.'
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
