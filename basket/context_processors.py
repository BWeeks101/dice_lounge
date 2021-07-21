from django.conf import settings
from decimal import Decimal
from django.contrib import messages
from products.models import Product


def basket_contents(request):
    basket_items = []
    errors = 0
    total = 0
    product_count = 0
    basket = request.session.get('basket', {})

    for product_id, quantity in basket.items():
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            product = None
            basket.items.pop(product_id)
            messages.error(
                request,
                f'Product ({product_id}) not found.  Removed from basket.',
                'from__basket_contents_basket'
            )

        if product is not None:
            max_per_purchase = product.max_per_purchase
            if max_per_purchase > product.stock:
                max_per_purchase = product.stock
            subtotal = quantity * product.price
            total += subtotal
            if quantity > product.stock:
                errors += 1
            product_count += quantity
            basket_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'product': product,
                'max_per_purchase': max_per_purchase,
                'stock': product.stock,
                'stock_state': product.stock_state,
                'subtotal': subtotal
            })

    # ...............................................Modified Boutique-Ado Code
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / 100
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    request.session['basket_errors'] = errors

    context = {
        'basket': {
            'items': basket_items,
            'errors': errors,
            'total': total,
            'product_count': product_count,
            'delivery': delivery,
            'free_delivery_delta': free_delivery_delta,
            'grand_total': grand_total
        },
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD
    }
    # ...........................................End Modified Boutique-Ado Code

    if 'removed_item' in request.session:
        session_removed_item = request.session.get('removed_item', {})
        request.session.pop('removed_item')
        try:
            removed_product = Product.objects.get(
                pk=session_removed_item['product_id'])
        except Product.DoesNotExist:
            removed_product = None

        removed_item = {
            'product_id': session_removed_item['product_id'],
            'quantity': session_removed_item['qty']
        }

        if removed_product is not None:
            removed_subtotal = (
                session_removed_item['qty'] * removed_product.price
            )
            removed_item.update({
                'product': removed_product,
                'subtotal': removed_subtotal
            })

        context['basket']['removed_item'] = removed_item

    return context
