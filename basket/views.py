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
            return redirect('/products/search_results/?q=' + request.GET['q'])

    return render(request, 'basket/basket.html')


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
            'Unable to update basket.  Product not found.'
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
                    basket[product_id] += quantity
                    if basket[product_id] > max_per_purchase:
                        basket[product_id] = max_per_purchase
                        messages.info(
                            request,
                            f'No more than {max_per_purchase} of ' +
                            f'{product.name} may be added to an order.'
                        )
                    messages.success(
                        request,
                        f'Adjusted {product.name} quantity to ' +
                        f'{basket[product_id]}.'
                    )
                else:
                    if quantity > max_per_purchase:
                        quantity = max_per_purchase
                        messages.info(
                            request,
                            f'No more than {max_per_purchase} of ' +
                            f'{product.name} may be added to an order.'
                        )
                    basket[product_id] = quantity
                    messages.success(
                        request,
                        f'Added {quantity}x {product.name} to your basket.'
                    )
                request.session['basket'] = basket
            else:
                messages.info(
                    request,
                    'Unable to update basket.  You may not add a quantity ' +
                    'of less than 1.'
                )
        else:
            messages.info(
                request,
                f'Unable to add {product.name} to basket.  Insufficient stock.'
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
            'Product not found.'
        )

    basket = request.session.get('basket', {})
    if product_id in basket:
        try:
            basket.pop(product_id)

            msg = 'Removed item from your basket.'
            if product is not None:
                msg = f'Removed {product.name} from your basket.'

            messages.success(request, msg)

            request.session['basket'] = basket
            status = 200
        except Exception as e:
            messages.error(request, f'Error removing product: {e}.')
            status = 500
    else:
        msg = 'Item is not in your basket.'
        if product is not None:
            msg = f'{product.name} is not in your basket.'
        messages.info(request, msg)
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
            'Product not found.'
        )

    basket = request.session.get('basket', {})

    if product is not None:
        quantity = int(request.POST.get('quantity'))

        max_per_purchase = product.max_per_purchase
        if max_per_purchase > product.stock:
            max_per_purchase = product.stock

        if quantity > 0 and max_per_purchase > 0:
            if quantity > max_per_purchase:
                quantity = max_per_purchase
                messages.info(
                    request,
                    f'No more than {max_per_purchase} of {product.name} may ' +
                    'be added to an order.'
                )
            basket[product_id] = quantity
            messages.success(
                request,
                f'Adjusted {product.name} quantity to {basket[product_id]}.'
            )
        elif quantity < 1:
            basket.pop(product_id)
            messages.success(
                request,
                f'Removed {product.name} from your basket.'
            )
        elif max_per_purchase < 1:
            basket.pop(product_id)
            messages.info(
                request,
                f'Unable to update quantity of {product.name} due to ' +
                'insufficient stock.'
            )
    else:
        if product_id in basket:
            basket.pop(product_id)
            messages.error(
                request,
                f'Removed non-existant product {product_id} from your ' +
                'basket.'
            )

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))
