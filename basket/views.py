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
            f'Unable to update basket.  Product ({product_id}) not found.',
            'from__add_to_basket'
        )

    if product is not None:
        if product.stock > 0:
            quantity = request.POST.get('quantity')
            if quantity is not None:
                quantity = int(quantity)
            if quantity > 0:
                basket = request.session.get('basket', {})
                max_per_purchase = product.max_per_purchase
                if max_per_purchase > product.stock:
                    max_per_purchase = product.stock
                if product_id in basket:
                    if basket[product_id] >= max_per_purchase:
                        messages.error(
                            request,
                            f'No more than {max_per_purchase} of ' +
                            f'{product.name} may be added to an order.',
                            f'from__add_to_basket,id__{product_id}'
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
                                f'from__add_to_basket,id__{product_id}'
                            )
                        else:
                            messages.success(
                                request,
                                f'Increased {product.name} quantity to ' +
                                f'{basket[product_id]}.',
                                f'from__add_to_basket,id__{product_id}'
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
                            f'from__add_to_basket,id__{product_id}'
                        )
                    else:
                        messages.success(
                            request,
                            f'Added {quantity}x {product.name} to your ' +
                            'basket.',
                            f'from__add_to_basket,id__{product_id}'
                        )
                    basket[product_id] = quantity
                request.session['basket'] = basket
            else:
                msg = f'You may not add {product.name} with a quantity of '
                msg += 'less than 1.'
                if quantity is None:
                    msg = f'No quantity supplied for {product.name}.'
                messages.error(
                    request,
                    'Unable to update basket.  ' + msg,
                    'from__add_to_basket'
                )
        else:
            messages.error(
                request,
                f'Unable to add {product.name} to basket.  Insufficient ' +
                'stock.',
                f'from__add_to_basket,id__{product_id}'
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
            f'Product ({product_id}) not found.',
            'from__remove_from_basket'
        )

    basket = request.session.get('basket', {})
    if product_id in basket:
        try:
            qty = basket[product_id]
            basket.pop(product_id)

            if product is not None:
                messages.success(
                    request,
                    f'Removed {qty}x {product.name} from your basket.',
                    f'from__remove_from_basket,id__{product_id}'
                )

                request.session['basket'] = basket
                request.session['removed_item'] = {
                    'product_id': product_id,
                    'qty': qty
                }
            else:
                messages.error(
                    request,
                    f'Removed non-existant product ({product_id}) from your ' +
                    'basket.',
                    'from__remove_from_basket'
                )
            status = 200
        except Exception as e:
            msg = f'Error removing non-existant product ({product_id}): {e}.',
            extra_tags = 'from__remove_from_basket'
            if product is not None:
                msg = f'Error removing product ({product_id}): {e}.',
                extra_tags += f',id__{product_id}'
            messages.error(request, msg, extra_tags)
            status = 500
    else:
        msg = f'Non-existant product ({product_id})'
        if product is not None:
            msg = f'{product.name}'
        messages.info(
            request,
            msg + ' was already removed from your basket.',
            'from__remove_from_basket')
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
            f'Product ({product_id}) not found.',
            'from__adjust_basket'
        )

    basket = request.session.get('basket', {})

    if product is not None:
        quantity = request.POST.get('quantity')
        if quantity is not None:
            quantity = int(quantity)

        max_per_purchase = product.max_per_purchase
        if max_per_purchase > product.stock:
            max_per_purchase = product.stock

        if quantity > 0 and max_per_purchase > 0:
            if quantity == basket[product_id]:
                messages.info(
                    request,
                    f'Your basket already contains {quantity}x ' +
                    f'{product.name}.',
                    f'from__adjust_basket,id__{product_id}'
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
                        f'from__adjust_basket,id__{product_id}'
                    )
                else:
                    adjustment = 'Increased'
                    if quantity < basket[product_id]:
                        adjustment = 'Reduced'
                    messages.success(
                        request,
                        f'{adjustment} {product.name} quantity to ' +
                        f'{quantity}.',
                        f'from__adjust_basket,id__{product_id}'
                    )
                basket[product_id] = quantity
        elif quantity is None:
            messages.error(
                request,
                'Unable to update basket.  No quantity supplied for ' +
                f'{product.name}.',
                'from__adjust_basket'
            )
        elif quantity < 1:
            qty = basket[product_id]
            basket.pop(product_id)
            messages.success(
                request,
                f'Removed {qty}x {product.name} from your ' +
                'basket.',
                f'from__adjust_basket,id__{product_id}'
            )
        elif max_per_purchase < 1:
            basket.pop(product_id)
            messages.info(
                request,
                f'Unable to update quantity of {product.name} due to ' +
                'insufficient stock.',
                f'from__adjust_basket,id__{product_id}'
            )
    else:
        if product_id in basket:
            basket.pop(product_id)
            messages.info(
                request,
                f'Removed non-existant product ({product_id}) from your ' +
                'basket.',
                'from__adjust_basket'
            )
        else:
            messages.info(
                request,
                f'Non-existant product ({product_id}) was already removed ' +
                'from your basket.',
                'from__adjust_basket')

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))
