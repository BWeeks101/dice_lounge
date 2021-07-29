from django.contrib import admin
from .models import (
    Product_Line, Category, Genre, Publisher, Sub_Product_Line, Product,
    Stock_State, Reduced_Reason
)


# Classes
class Product_LineAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'genre',
        'publisher',
        'hidden'
    )

    search_fields = (
        'id',
        'identifier',
        'name',
        'description',
        'publisher__name',
        'publisher__identifier',
        'category__name',
        'category__identifier',
        'genre__name',
        'genre__identifier'
    )

    ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'identifier'
    )

    ordering = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'identifier'
    )

    ordering = ('name',)


class PublisherAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'identifier'
    )

    ordering = ('name',)


class Sub_Product_LineAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'product_line',
        'hidden'
    )

    search_fields = (
        'id',
        'identifier',
        'name',
        'product_line__name',
        'product_line__identifier',
        'product_line__publisher__name',
        'product_line__publisher__identifier',
        'product_line__category__name',
        'product_line__category__identifier',
        'description'
    )

    ordering = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        '_sub_product_line',
        '_product_line',
        'price',
        'stock_state',
        'stock',
        'hidden'
    )

    search_fields = (
        'id',
        'identifier',
        'sub_product_line__name',
        'sub_product_line__identifier',
        'sub_product_line__product_line__name',
        'sub_product_line__product_line__identifier',
        'sub_product_line__product_line__publisher__name',
        'sub_product_line__product_line__publisher__identifier',
        'sub_product_line__product_line__category__name',
        'sub_product_line__product_line__category__identifier',
        'name',
        'description'

    )

    # _sub_product_line() based on the following example by Tim Kamanin:
    # https://timonweb.com/django/how-to-sort-django-admin-list-column-by-a-value-from-a-related-model/
    def _sub_product_line(self, obj):
        return obj.sub_product_line.name

    _sub_product_line.admin_order_field = 'sub_product_line__name'
    _sub_product_line.short_description = 'Sub Product Line'

    # _product_line() based on the following example by Tim Kamanin:
    # https://timonweb.com/django/how-to-sort-django-admin-list-column-by-a-value-from-a-related-model/
    def _product_line(self, obj):
        return obj.sub_product_line.product_line

    _product_line.admin_order_field = 'sub_product_line__product_line'
    _product_line.short_description = 'Product Line'

    ordering = (
        'name',
        _sub_product_line.admin_order_field,
        _product_line.admin_order_field,
    )


class Stock_StateAdmin(admin.ModelAdmin):
    list_display = (
        'state',
        'identifier',
        'available'
    )

    ordering = ('state',)


class Reduced_ReasonAdmin(admin.ModelAdmin):
    list_display = (
        'reason',
        'identifier',
        'default_reduction_percentage'
    )

    ordering = ('reason',)


# Register your models here.
admin.site.register(Product_Line, Product_LineAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Sub_Product_Line, Sub_Product_LineAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock_State, Stock_StateAdmin)
admin.site.register(Reduced_Reason, Reduced_ReasonAdmin)
