from django.shortcuts import render
from django.conf import settings


def custom_error_403(request, exception):
    context = {
        'title': 'Mothra says No!',
        'error': "You don't have permission to access this page.  Did you \
            forget to login?"
    }
    return render(request, 'error.html', context)


def custom_error_404(request, exception):
    context = {
        'title': 'Oops...',
        'error': 'It looks like a bug crept into the system!  It either ate a \
            record, got stuck in a relay or otherwise made a nuisance of \
                itself.  Unfortunately, that resource cannot be found.'
    }
    return render(request, 'error.html', context)


def custom_error_500(request):
    context = {
        'title': 'Well this is embarrassing...',
        'error': f'It looks like a bug crept into the system!  It either ate \
            a record, got stuck in a relay or otherwise made a nuisance of \
                itself.  Please refresh the page and try again.  If the \
                    problem persists, please contact us: \
                        {settings.DEFAULT_SUPPORT_EMAIL}'
    }
    return render(request, 'error.html', context)
