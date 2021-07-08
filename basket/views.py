from django.shortcuts import redirect, render, reverse, HttpResponse
from django.contrib import messages
from products.models import Product


# Create your views here.
def view_basket(request):
    """
        A view that renders the basket contents page
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect(
                reverse('search_results') + '?q=' + request.GET['q'] +
                '&redirect_url=' + request.GET.get('redirect_url')
            )

    context = {
        'view': 'basket'
    }

    return render(request, 'basket/basket.html', context)


def add_to_basket(request, product_id):
    """
        Add a quantity of the specified product to the basket
    """

    redirect_url = request.POST.get('redirect_url')
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        product = None
        messages.error(
            request,
            'Unable to update basket.  Product not found.',
            'sender_add_to_basket'
        )

    if product is not None:
        if product.stock > 0:
            quantity = int(request.POST.get('quantity'))
            if quantity > 0:
                basket = request.session.get('basket', {})
                max_per_purchase = product.max_per_purchase
                if max_per_purchase > product.stock:
                    max_per_purchase = product.stock
                if product_id in basket:
                    if basket[product_id] >= max_per_purchase:
                        messages.info(
                            request,
                            f'No more than {max_per_purchase} of ' +
                            f'{product.name} may be added to an order.',
                            f'sender_add_to_basket,id_{product_id}'
                        )
                    else:
                        basket[product_id] += quantity
                        if basket[product_id] > max_per_purchase:
                            basket[product_id] = max_per_purchase
                            messages.info(
                                request,
                                f'No more than {max_per_purchase} of ' +
                                f'{product.name} may be added to an order.  ' +
                                f'Increased {product.name} quantity to ' +
                                f'{basket[product_id]}.',
                                f'sender_add_to_basket,id_{product_id}'
                            )
                        else:
                            messages.success(
                                request,
                                f'Increased {product.name} quantity to ' +
                                f'{basket[product_id]}.',
                                f'sender_add_to_basket,id_{product_id}'
                            )
                else:
                    if quantity > max_per_purchase:
                        quantity = max_per_purchase
                        messages.info(
                            request,
                            f'No more than {max_per_purchase} of ' +
                            f'{product.name} may be added to an order.  ' +
                            f'Added {quantity}x {product.name} to your ' +
                            'basket.',
                            f'sender_add_to_basket,id_{product_id}'
                        )
                    else:
                        messages.success(
                            request,
                            f'Added {quantity}x {product.name} to your ' +
                            'basket.',
                            f'sender_add_to_basket,id_{product_id}'
                        )
                    basket[product_id] = quantity
                request.session['basket'] = basket
            else:
                messages.info(
                    request,
                    'Unable to update basket.  You may not add a quantity ' +
                    'of less than 1.',
                    f'sender_add_to_basket,id_{product_id}'
                )
        else:
            messages.info(
                request,
                f'Unable to add {product.name} to basket.  Insufficient ' +
                'stock.',
                f'sender_add_to_basket,id_{product_id}'
            )
    if redirect_url is None:
        return redirect(reverse('view_basket'))
    return redirect(redirect_url)


def remove_from_basket(request, product_id):
    """
        Remove the specified product from the basket
    """
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        product = None
        messages.error(
            request,
            'Product not found.',
            'sender_remove_from_basket'
        )

    basket = request.session.get('basket', {})
    if product_id in basket:
        try:
            qty = basket[product_id]
            basket.pop(product_id)

            msg = 'Removed item from your basket.'
            if product is not None:
                msg = f'Removed {qty}x {product.name} from your basket.'

            messages.success(
                request,
                msg,
                f'sender_remove_from_basket,id_{product_id}'
            )

            request.session['basket'] = basket
            request.session['removed_item'] = {
                'product_id': product_id,
                'qty': qty
            }
            status = 200
        except Exception as e:
            messages.error(
                request,
                f'Error removing product: {e}.',
                f'sender_remove_from_basket,id_{product_id}')
            status = 500
    else:
        msg = 'Item is not in your basket.'
        if product is not None:
            msg = f'{product.name} is not in your basket.'
        messages.info(request, msg, 'sender_remove_from_basket')
        status = 200

    return HttpResponse(status=status)


def adjust_basket(request, product_id):
    """
        Adjust quantity of the specified product to the specified amount
    """

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        product = None
        messages.error(
            request,
            'Product not found.',
            'sender_adjust_basket'
        )

    basket = request.session.get('basket', {})

    if product is not None:
        quantity = int(request.POST.get('quantity'))

        max_per_purchase = product.max_per_purchase
        if max_per_purchase > product.stock:
            max_per_purchase = product.stock

        if quantity > 0 and max_per_purchase > 0:
            if quantity == basket[product_id]:
                messages.info(
                    request,
                    f'Your basket already contains {quantity}x ' +
                    f'{product.name}.',
                    f'sender_adjust_basket,id_{product_id}'
                )
            else:
                if quantity > max_per_purchase:
                    quantity = max_per_purchase
                    messages.info(
                        request,
                        f'No more than {max_per_purchase} of {product.name} ' +
                        ' may be added to an order.  ' +
                        f'Adjusted {product.name} quantity to ' +
                        f'{quantity}.',
                        f'sender_adjust_basket,id_{product_id}'
                    )
                else:
                    adjustment = 'Increased'
                    if quantity < basket[product_id]:
                        adjustment = 'Reduced'
                    messages.success(
                        request,
                        f'{adjustment} {product.name} quantity to ' +
                        f'{quantity}.',
                        f'sender_adjust_basket,id_{product_id}'
                    )
                basket[product_id] = quantity
        elif quantity < 1:
            qty = basket[product_id]
            basket.pop(product_id)
            messages.success(
                request,
                f'Removed {qty}x {product.name} from your ' +
                'basket.',
                f'sender_adjust_basket,id_{product_id}'
            )
        elif max_per_purchase < 1:
            basket.pop(product_id)
            messages.info(
                request,
                f'Unable to update quantity of {product.name} due to ' +
                'insufficient stock.',
                f'sender_adjust_basket,id_{product_id}'
            )
    else:
        if product_id in basket:
            basket.pop(product_id)
            messages.error(
                request,
                f'Removed non-existant product {product_id} from your ' +
                'basket.',
                f'sender_adjust_basket,id_{product_id}'
            )

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))
