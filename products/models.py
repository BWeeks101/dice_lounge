from django.db import models


# Create your models here.
# From boutique ado sample project
class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Genre(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Publisher(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Stock_State(models.Model):
    state = models.CharField(max_length=254)
    friendly_state = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.state

    def get_friendly_state(self):
        return self.friendly_state


class Reduced_Reason(models.Model):
    reason = models.CharField(max_length=254)
    friendly_reason = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.reason

    def get_friendly_reason(self):
        return self.friendly_reason


class Product_Line(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL
    )
    genre = models.ForeignKey(
        'Genre', null=True, blank=True, on_delete=models.SET_NULL
    )
    publisher = models.ForeignKey(
        'Publisher', null=True, blank=True, on_delete=models.SET_NULL
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Sub_Product_Line(models.Model):
    product_line = models.ForeignKey(
        'Product_Line', null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    sub_product_line = models.ForeignKey(
        'sub_product_line', null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    reduced = models.BooleanField(null=False, blank=False)
    reduced_percentage = models.IntegerField()
    reduced_reason = models.ForeignKey(
        'Reduced_Reason', null=True, blank=True, on_delete=models.SET_NULL
    )
    stock_state = models.ForeignKey(
        'Stock_State', null=True, blank=True, on_delete=models.SET_NULL
    )
    stock = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    def get_stock(self):
        return {
            'stock_state': self.stock_state,
            'stock': self.stock
        }
