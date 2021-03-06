from django.contrib import admin
from .models import Order, OrderLineItem


# Register your models here.
# ...................................................Modified Boutique-Ado Code
class OrderLineItemAdminInLine(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = (
        'lineitem_total',
    )

    fields = (
        'product_id',
        'product',
        'sub_product_line',
        'product_line',
        'item_price',
        'quantity'
    )


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInLine,)

    readonly_fields = (
        'order_number',
        'user_profile',
        'email',
        'phone_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_basket',
        'stripe_pid'
    )

    fields = (
        'order_number',
        'user_profile',
        'email',
        'phone_number',
        'date',
        'delivery_first_name',
        'delivery_last_name',
        'delivery_address1',
        'delivery_address2',
        'delivery_town_or_city',
        'delivery_county',
        'delivery_postcode',
        'delivery_country',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_basket',
        'stripe_pid'
    )

    list_display = (
        'order_number',
        'date',
        'user_profile',
        'email',
        'phone_number',
        'delivery_first_name',
        'delivery_last_name',
        'delivery_postcode',
        'order_total',
        'delivery_cost',
        'grand_total'
    )

    search_fields = (
        'order_number',
        'date',
        'user_profile__user__username',
        'user_profile__user__first_name',
        'user_profile__user__last_name',
        'user_profile__user__email',
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
        'delivery_country',
        'order_total',
        'grand_total',
    )

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
# ...............................................End Modified Boutique-Ado Code
