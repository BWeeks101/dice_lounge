from django import template


register = template.Library()


@register.filter(name='strip_redirect_url')
def strip_redirect_url(request, **kwargs):
    """
        Return a complete url after stripping the redirect_url param
    """
    url = request.GET.copy()

    try:
        del url['redirect_url']
    except KeyError:
        pass

    return url.urlencode()
