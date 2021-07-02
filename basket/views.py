from django.shortcuts import redirect, render, reverse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from products.models import Product


# Create your views here.
def view_basket(request):
    """
        A view that renders the basket contents page
    """

    return render(request, 'basket/basket.html')


def add_to_basket(request, product_id):
    """
        Add a quantity of the specified product to the basket
    """

    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    basket = request.session.get('basket', {})

    if product_id in list(basket.keys()):
        basket[product_id] += quantity
        messages.success(
            request,
            f'Adjusted {product.name} quantity to {basket[product_id]}'
        )
    else:
        basket[product_id] = quantity
        messages.success(request, f'Added {product.name} to your basket')

    request.session['basket'] = basket
    return redirect(redirect_url)


def remove_from_basket(request, product_id):
    """
        Remove the specified product from the basket
    """

    product = get_object_or_404(Product, pk=product_id)

    try:
        basket = request.session.get('basket', {})

        basket.pop(product_id)
        messages.success(request, f'Removed {product.name} from your basket')

        request.session['basket'] = basket
        status = 200

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        status = 500

    return HttpResponse(status=status)


def adjust_basket(request, product_id):
    """
        Adjust quantity of the specified product to the specified amount
    """

    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))

    basket = request.session.get('basket', {})

    if quantity > 0:
        basket[product_id] = quantity
        messages.success(
            request,
            f'Adjusted {product.name} quantity to {basket[product_id]}'
        )
    else:
        basket.pop(product_id)
        messages.success(request, f'Removed {product.name} from your basket')

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))
