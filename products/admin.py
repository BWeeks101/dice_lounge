from django.contrib import admin
from .models import (
    Product_Line, Category, Genre, Publisher, Sub_Product_Line, Product,
    Stock_State, Reduced_Reason
)


# Classes
class Product_LineAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'category',
        'genre',
        'publisher'
    )

    ordering = ('friendly_name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name'
    )

    ordering = ('friendly_name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name'
    )

    ordering = ('friendly_name',)


class PublisherAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name'
    )

    ordering = ('friendly_name',)


class Sub_Product_LineAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'product_line'
    )

    ordering = ('friendly_name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'sub_product_line',
        'get_product_line',
        'price',
        'stock_state',
        'stock'
    )

    # Get_Product_Line() based on the following example by Tim Kamanin:
    # https://timonweb.com/django/how-to-sort-django-admin-list-column-by-a-value-from-a-related-model/
    def get_product_line(self, obj):
        return obj.sub_product_line.product_line

    get_product_line.admin_order_field = 'sub_product_line__product_line'
    get_product_line.short_description = 'Product Line'

    ordering = ('sub_product_line', 'friendly_name',)


class Stock_StateAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_state',
        'state'
    )

    ordering = ('friendly_state',)


class Reduced_ReasonAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_reason',
        'reason'
    )

    ordering = ('friendly_reason',)


# Register your models here.
admin.site.register(Product_Line, Product_LineAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Sub_Product_Line, Sub_Product_LineAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock_State, Stock_StateAdmin)
admin.site.register(Reduced_Reason, Reduced_ReasonAdmin)
