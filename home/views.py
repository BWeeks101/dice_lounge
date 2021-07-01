from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    """
        A view to return the index page or redirect a search
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect('/products/search_results/?q=' + request.GET['q'])

    return render(request, 'home/index.html')
