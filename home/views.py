from django.shortcuts import render, redirect
from products.views import get_search_request


# Create your views here.
def home(request):
    """
        A view to return the home page or redirect a search
    """

    # Redirect search requests
    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    # Add the view to the context
    context = {
        'view': 'home'
    }

    # Redirect to the home page, passing the context
    return render(request, 'home/index.html', context)
