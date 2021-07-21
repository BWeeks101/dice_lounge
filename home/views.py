from django.shortcuts import render, redirect
from products.views import get_search_request


# Create your views here.
def home(request):
    """
        A view to return the home page or redirect a search
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    context = {
        'view': 'home'
    }

    return render(request, 'home/index.html', context)
