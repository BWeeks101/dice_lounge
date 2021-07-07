from django.shortcuts import render, redirect, reverse


# Create your views here.
def index(request):
    """
        A view to return the index page or redirect a search
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect(
                reverse('search_results') + '?q=' + request.GET['q'] +
                '&redirect_url=' + request.GET.get('redirect_url')
            )

    return render(request, 'home/index.html')
