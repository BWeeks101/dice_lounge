from django import template


register = template.Library()


@register.filter(name='strip_redirect_url')
def strip_redirect_url(request, **kwargs):
    """
        Return a complete url after stripping any redirect_url and
        redirect_params parameters
    """
    # Get a copy of the request.GET queryDict so that it is mutable
    url = request.GET.copy()

    # delete the redirect_url and redirect_params parameters if they exist
    try:
        del url['redirect_url']
        del url['redirect_params']
    except KeyError:
        pass

    # return the updated url
    return url.urlencode()


@register.filter(name='format_redirect_params')
def format_redirect_params(request, **kwargs):
    """
        Reformat parameters from a url into multiple instances of the
        redirect_params parameter, with values equating to the original
        param + value.

        ie:
            sort=name&direction=asc
        becomes:
            redirect_params=sort=name&redirect_params=direction=asc

        This allows the redirect params to be interpreted by the server as a
        list, and correctly passed to the search_results view, where they can
        be appended to the redirect_url to correctly redirect on search
        failure.
    """
    # Get a copy of the request.GET queryDict so that it is mutable
    url = request.GET.copy()

    new_params = []
    del_keys = []

    # Iterate over the url parameters.  Add param_keys to the del_keys list.
    # Add a new object to new_params with its own key of 'redirect_params' and
    # its value as param_key=param_value
    for param_key, param_value in url.items():
        del_keys.append(param_key)
        new_params.append({'redirect_params': param_key + '=' + param_value})

    # Iterate over the del_keys list and delete the keys from the url
    for key in del_keys:
        try:
            del url[key]
        except KeyError:
            pass

    # Iterate over the new_params list and add the objects to the url
    for param in new_params:
        url.update(param)

    # return the updated url
    return url.urlencode()
