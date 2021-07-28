from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from .models import (Product_Line, Reduced_Reason, Stock_State,
                     Sub_Product_Line, Product, Category, Genre, Publisher)
from .forms import (Category_Form, Genre_Form, Product_Form, Product_Line_Form,
                    Publisher_Form, Reduced_Reason_Form, Stock_State_Form,
                    Sub_Product_Line_Form)

# Create your views here.


# Build data to populate Sort dropdown lists
def build_sort_options(sort_list, with_reset_option=True):
    '''
        Take a list of field names and convert them into object pairs used to
        populate Sort dropdown lists

        List Item Format:
            <field>::<direction-descriptor>

        Valid direction-descriptors:
            az = (A-Z) (Default)
            lh = (Low to High)

        If a direction-descriptor is not provided, az is assumed.
        For example:
            name::az

            or

            name

        Will both produce an object with the following properties:
            {
                a = {
                    'url': 'sort=name&direction=asc'
                    'value': 'name_asc'
                    'text': 'Name (A-Z)'
                }
                b = {
                    'url': 'sort=name&direction=desc'
                    'value': 'name_desc'
                    'text': 'Name (Z-A)'
                }
            }

        This object is appended to sort_options.list and returned.

        More complex field values are supported (ie, when sorting with joins):
            <field__field__field>::<direction-descriptor>

        For example:
            sub_prd__*product_line__name::az

        In this example, the * is used to denote that the text until the next
        __ will be utilised to construct the text string.  (The * will be
        stripped from the url and value strings).  The resulting object will be
        produced:
            {
                a = {
                    'url': 'sort=sub_prd__product_line__name_az&direction=asc'
                    'value': 'sub_prd__product_line__name_az_asc'
                    'text': 'Product Line (A-Z)'
                }
                b = {
                    'url': 'sort=sub_prd__product_line__name_az&direction=desc'
                    'value': 'sub_prd__product_line__name_az_desc'
                    'text': 'Product Line (Z-A)'
                }
            }

        Multiple * can be used to construct the text string.  For example:
            sub_product_line__*product_line__*name::az

        Would create the following text strings:
            Product Line Name (A-Z)
            Product Line Name (Z-A)


        The function returns the following object:
            sort_options = {
                'reset': {
                    'value': 'None_None',
                    'text': 'Sort by...'
                }
                'list': [
                    {
                        'a': {
                            'url'
                            'value'
                            'text'
                        },
                        'b': {
                            'url'
                            'value'
                            'text'
                        }
                    },
                    {}...
                ]
            }

        The function has an optional parameter:
            with_reset_option: (Default: True)

        When set to false, the sort_options object will be returned *without*
        the 'reset' object.

        (The 'reset' object is used to populate the default 'Sort by..'
        dropdown option, which is used to clear other Sorts)
    '''
    sort_options = {'list': []}

    if with_reset_option:
        sort_options.update({
            'reset': {
                'value': 'None_None',
                'text': 'Sort by...'
            }
        })

    for option in sort_list:
        if '::' not in option:
            option += '::az'
        option = option.lower().rsplit('::', 1)
        text = ''
        words = []
        if '__' in option[0]:
            fields = option[0].split('__')
            for field in fields:
                if field[0] == '*':
                    words += field.split('*')[1].split('_')
        else:
            words = option[0].split('_')

        option[0] = option[0].replace('*', '')
        for word in words:
            text += word.capitalize() + ' '
        text = text.strip()
        if option[1] == 'lh':
            text_suffix = ['Low', ' to ', 'High']
        else:
            text_suffix = ['A', '-', 'Z']
        sort_option_a = {
            'url': 'sort=' + option[0] + '&direction=asc',
            'value': option[0] + '_asc',
            'text': (
                text + ' (' + text_suffix[0] +
                text_suffix[1] + text_suffix[2] + ')'
            )
        }
        sort_option_b = {
            'url': 'sort=' + option[0] + '&direction=desc',
            'value': option[0] + '_desc',
            'text': (
                text + ' (' + text_suffix[2] +
                text_suffix[1] + text_suffix[0] + ')'
            )
        }
        sort_option = {'a': sort_option_a, 'b': sort_option_b}
        sort_options['list'].append(sort_option)

    return sort_options


# Apply search query to the Product model and return dataset
def apply_query(query):
    '''
        Execute queries for user provided search string over key model fields
        and return the dataset

        Product:
            Name
            Identifier
            Description
        Sub Product Line:
            Name
            Identifier
            Description
        Product Line:
            Name
            Identifier
            Description
        Publisher:
            Name
            Identifier

        NB: Identifiers have been included because they often contain common
        abbreviations familiar to shoppers, for example:

        Wizards of the Coast are often referred to as 'wotc'
        Age of Sigmar is often referred to as 'aos'
    '''
    queries = (Q(name__icontains=query) |
               Q(identifier__icontains=query) |
               Q(description__icontains=query) |
               Q(sub_product_line__name__icontains=query) |
               Q(sub_product_line__identifier__icontains=query) |
               Q(sub_product_line__description__icontains=query) |
               Q(sub_product_line__product_line__name__icontains=query) |
               Q(sub_product_line__product_line__identifier__icontains=query) |
               Q(**{
                   'sub_product_line__product_line__description' +
                   '__icontains': query
                   }) |
               Q(**{
                   'sub_product_line__product_line__publisher__name' +
                   '__icontains': query
                   }) |
               Q(**{
                   'sub_product_line__product_line__publisher__identifier' +
                   '__icontains': query
                   }))
    return Product.objects.filter(queries)


# Filter hidden products from the dataset
def exclude_hidden_products(dataset):
    dataset = dataset.exclude(hidden=True).exclude(
        sub_product_line__hidden=True).exclude(
            sub_product_line__product_line__hidden=True)

    return dataset


# Apply selected sort to dataset
def apply_sort(dataset, request, view=None):
    '''
        Apply specified sort to dataset and return it along with a generated
        sort key describing the sort field and direction
    '''

    dataset = exclude_hidden_products(dataset)

    sortkey = None
    direction = None

    if 'sort' in request.GET:
        sortkey = request.GET['sort']
    else:
        sortkey = 'name'

    sortkeys = {
        'name': 'lower_name',
        'price': 'reduced_price',
        'stock': 'stock_state__state',
        'product_line': 'sub_product_line__product_line__name',
        'genre': 'genre__identifier',
        'category': 'sub_product_line__name',
        'publisher': 'sub_product_line__product_line__publisher__name'
    }

    if view == 'all_games':
        sortkeys.update({
            'category': 'category__identifier',
            'publisher': 'publisher__identifier'
        })

    sort_key = sortkeys.get(sortkey)

    if sort_key is None:
        sort_key = sortkey

    if sort_key == 'lower_name':
        dataset = dataset.annotate(lower_name=Lower('name'))

    if 'direction' in request.GET:
        direction = request.GET['direction']

    if direction == 'desc':
        sort_key = f'-{sort_key}'
    else:
        direction = 'asc'

    dataset = dataset.order_by(sort_key)

    applied_sort = f'{sortkey}_{direction}'

    return {
        'applied_sort': applied_sort,
        'dataset': dataset
    }


# Apply filters to dataset
def apply_filters(dataset, request, view=None):
    '''
        Apply specified filters to dataset and return it, along with the
        identifier field for active filter values
    '''

    filters = {
        'stock': 'stock_state',
        'category': 'sub_product_line',
        'product_line': 'sub_product_line__product_line',
        'genre': 'genre',
        'publisher': 'sub_product_line__product_line__publisher',
        'reduced_reason': 'reduced_reason'
    }

    if view == 'all_games':
        filters.update({
            'category': 'category',
            'publisher': 'publisher'
        })

    stock_states = None
    categories = None
    product_lines = None
    genres = None
    publishers = None
    reduced_reasons = None
    filter_count = 0

    if 'stock' in request.GET:
        stock_states = request.GET['stock'].split(',')
        filter_count += len(stock_states)
        dataset = dataset.filter(**{
            filters.get('stock') + '__identifier__in': stock_states
        })
        stock_states = Stock_State.objects.filter(
            identifier__in=stock_states).values('identifier')

    if 'category' in request.GET:
        categories = request.GET['category'].split(',')
        filter_count += len(categories)
        dataset = dataset.filter(**{
            filters.get('category') + '__identifier__in': categories
        })
        if view == 'all_games':
            categories = Category.objects.filter(
                identifier__in=categories).values('identifier')
        else:
            categories = Sub_Product_Line.objects.exclude(hidden=True).exclude(
                product_line__hidden=True).filter(
                    identifier__in=categories).values('identifier')

    if 'product_line' in request.GET:
        product_lines = request.GET['product_line'].split(',')
        filter_count += len(product_lines)
        dataset = dataset.filter(**{
            filters.get('product_line') + '__identifier__in': product_lines
        })
        product_lines = Product_Line.objects.exclude(hidden=True).filter(
            identifier__in=product_lines).values('identifier')

    if 'genre' in request.GET:
        genres = request.GET['genre'].split(',')
        filter_count += len(genres)
        dataset = dataset.filter(**{
            filters.get('genre') + '__identifier__in': genres
        })
        genres = Genre.objects.filter(identifier__in=genres).values(
            'identifier')

    if 'publisher' in request.GET:
        publishers = request.GET['publisher'].split(',')
        filter_count += len(publishers)
        dataset = dataset.filter(**{
            filters.get('publisher') + '__identifier__in': publishers
        })
        publishers = Publisher.objects.filter(
            identifier__in=publishers).values('identifier')

    if 'reduced_reason' in request.GET:
        reduced_reasons = request.GET['reduced_reason'].split(',')
        filter_count += len(reduced_reasons)
        dataset = dataset.filter(**{
            filters.get('reduced_reason') + '__identifier__in': reduced_reasons
        })
        reduced_reasons = Reduced_Reason.objects.filter(
            identifier__in=reduced_reasons).values('identifier')

    return {
        'dataset': dataset,
        'filter_count': filter_count,
        'stock': stock_states,
        'categories': categories,
        'product_lines': product_lines,
        'genres': genres,
        'publishers': publishers,
        'reduced_reasons': reduced_reasons
    }


# Apply sort and filters to dataset
def apply_sort_and_filters(dataset, request, view=None):
    '''
        Apply selected sort and filters to dataset and return it, along with
        a generated sort key describing the sort field and direction, and the
        identifier field for active filter values
    '''
    results = apply_sort(dataset, request, view)
    applied_sort = results['applied_sort']
    results = apply_filters(results['dataset'], request, view)
    results.update({
        'applied_sort': applied_sort
    })

    return results


# Return paginated dataset
def apply_pagination(context, dataset_key, page=1, num_products_per_page=12):
    '''
        Paginate a dataset, creating pages of 12, 24, 48 or 96 objects as
        requested, then return the requested page of results along with key
        values representing the applied pagination:
            page number
            number of products per page
            products per page options (used to build dropdown list)
            number of page links to display at once in pagination controls
            page control range (first to last page to generate a page link for)
    '''

    try:
        num_products_per_page = int(num_products_per_page)
    except ValueError:
        num_products_per_page = 12

    pagination = {
        'page': page,
        'num_products_per_page': num_products_per_page,
        'products_per_page_options': [12, 24, 48, 96]
    }

    if (pagination['num_products_per_page'] not in
            pagination['products_per_page_options']):
        pagination['num_products_per_page'] = 12

    dataset = context[dataset_key]

    paginator = Paginator(dataset, pagination['num_products_per_page'])
    try:
        dataset = paginator.page(pagination['page'])
    except PageNotAnInteger:
        dataset = paginator.page(1)
        pagination['page'] = 1
    except EmptyPage:
        if int(pagination['page']) < 1:
            dataset = paginator.page(1)
            pagination['page'] = 1
        else:
            dataset = paginator.page(paginator.num_pages)
            pagination['page'] = int(paginator.num_pages)

    pagination.update({
        'page': int(pagination['page']),
        'num_products': int(paginator.count),
        'num_pages': int(paginator.num_pages),
        'num_page_controls': 6,
    })

    if pagination['page'] > 1:
        pagination['num_page_controls'] -= 1

    if pagination['page'] < (
            pagination['num_pages'] - (pagination['num_page_controls'] - 1)):
        pagination['num_page_controls'] -= 1

    start_page = 1
    stop_page = pagination['num_page_controls']
    if pagination['num_pages'] <= pagination['num_page_controls']:
        stop_page = pagination['num_pages']

    if pagination['num_pages'] > pagination['num_page_controls']:
        if pagination['page'] > pagination['num_page_controls']:
            if (pagination['num_pages'] - (
                    pagination['num_page_controls'] - 1)) < pagination['page']:
                start_page = pagination['num_pages'] - (
                    pagination['num_page_controls'] - 1)
                stop_page = pagination['num_pages'] + 1
            else:
                start_page = pagination['page']
                stop_page = start_page + (pagination['num_page_controls'])
        else:
            start_page = pagination['page']
            stop_page = start_page + (pagination['num_page_controls'])

    if (stop_page == pagination['num_pages'] and
            pagination['num_pages'] <= pagination['num_page_controls']):
        stop_page += 1

    pagination.update({
        'page_control_range': range(start_page, stop_page)
    })

    context.update({
        dataset_key: dataset,
        'pagination': pagination
    })

    return context


# Check if a sub_product_line should appear 'hidden'
# If the sub_product_line is hidden, or it's product line is hidden, return
# true
# Requires either a queryset object, or a dict that contains the id of the
# sub_product_line
def is_sub_product_line_hidden(sub_product_line):
    if type(sub_product_line) is dict:
        id = sub_product_line['id']
        sub_product_line = Sub_Product_Line.objects.get(id=id)

    if (sub_product_line.hidden is True or
            sub_product_line.product_line.hidden is True):
        return True

    return False


# Check if a product should appear 'hidden'
# If the product is hidden, or it's sub product line or product line are
# hidden, return true.
# Requires either a queryset object, or a dict that contains the id of the
# product
def is_product_hidden(product):
    if type(product) is dict:
        id = product['id']
        product = Product.objects.get(id=id)

    if (product.hidden is True or
        product.sub_product_line.hidden is True or
            product.sub_product_line.product_line.hidden is True):
        return True

    return False


# Set an instance of a product to 0 stock, 0 available for purchase and change
# it's stock state to no longer available.
# NB: This is *not* saved to the DB.  It is a change to the live instance only.
def set_product_instance_unavailable(product):
    product.stock = 0
    product.max_per_purchase = 0
    no_longer_available = Stock_State.objects.get(
        identifier='no_longer_available')
    product.stock_state = no_longer_available

    return product


# Adjust max_per_purchase by stock
# NB: Converts a QuerySet into a List, and returns a List
def adjust_max_per_purchase(products):
    products = list(products)
    for product in products:
        if product.max_per_purchase > product.stock:
            product.max_per_purchase = product.stock

    return products


# format request for redirection to search_results
def get_search_request(request):
    url = reverse('search_results') + '?q=' + request.GET['q']

    redirect_url = request.GET.get('redirect_url')
    if redirect_url is None:
        return url

    url += '&redirect_url=' + redirect_url

    redirect_params = request.GET.get('redirect_params')
    if redirect_params is not None and len(redirect_params) > 0:
        url += '&' + redirect_params

    return url


# Return search results
def search_results(request):
    """
        A view to show all products in a set of search results,
        including sorting, filtering and pagination
    """

    if request.GET:

        # format redirection url
        def get_redirect_url(request=request):
            url = request.GET.get('redirect_url')

            if url is None:
                return reverse('all_games')

            redirect_params = request.GET.getlist('redirect_params')

            if len(redirect_params) == 0:
                return url

            params = f'?{redirect_params[0]}'
            for param in range(1, len(redirect_params)):
                params += '&' + redirect_params[param]

            url += params

            return url

        # Strip leading/trailing whitespace, then get up to 254 chars of the
        # query parameter
        query = request.GET['q'].strip()[:254]

        # If no query parameter, send a message and redirect
        if not query:
            messages.error(
                request,
                "You didn't enter any search criteria",
                'from__search'
            )
            return redirect(get_redirect_url())

        if len(query) < 3:
            messages.error(
                request,
                "Please enter a search term of at least 3 characters",
                'from__search'
            )
            return redirect(get_redirect_url())

        # Apply the query to the Product table, then sort the results
        sort_and_filter = apply_sort(
            apply_query(query), request)

        # If no results, send a message and redirect
        if len(sort_and_filter['dataset']) == 0:
            messages.info(
                request,
                "No results found.  Please try another search term.",
                'from__search'
            )
            return redirect(get_redirect_url())

        sort_options = build_sort_options([
            'name',
            'price::lh',
            'product_line',
            'category',
            'publisher'
        ])

        product_lines = Product_Line.objects.filter(
                id__in=sort_and_filter['dataset'].values(
                    'sub_product_line__product_line__id')).order_by('name')
        filters = []
        for product_line in product_lines:
            filter = {
                'product_line': {
                    'identifier': product_line.identifier,
                    'name': product_line.name
                },
                'sub_product_lines': Sub_Product_Line.objects.filter(
                    id__in=sort_and_filter['dataset'].filter(
                        sub_product_line__product_line__id=product_line.id
                    ).values('sub_product_line__id')).values(
                            'identifier', 'name').order_by('name')
            }
            filters.append(filter)

        stock_states = Stock_State.objects.exclude(
            identifier='no_longer_available').filter(
                id__in=sort_and_filter['dataset'].values(
                    'stock_state__id')).values('id').order_by(
                        'id').distinct().values(
                            'identifier', 'state').order_by('state')

        reduced_reasons = Reduced_Reason.objects.filter(
            id__in=sort_and_filter['dataset'].values(
                'reduced_reason__id')).values('id').order_by(
                    'id').distinct().values(
                        'identifier', 'reason').order_by('reason')

        applied_sort = sort_and_filter['applied_sort']
        sort_and_filter = apply_filters(
            sort_and_filter['dataset'], request)
        sort_and_filter.update({
            'applied_sort': applied_sort
        })

        context = {
            'sort_options': sort_options,
            'view': 'search',
            'products': sort_and_filter['dataset'],
            'filters': filters,
            'stock_states': stock_states,
            'reduced_reasons': reduced_reasons,
            'search_term': query,
            'applied_filters': {
                'count': sort_and_filter['filter_count'],
                'categories': sort_and_filter['categories'],
                'product_lines': sort_and_filter['product_lines'],
                'publishers': sort_and_filter['publishers'],
                'stock': sort_and_filter['stock'],
                'reduced_reasons': sort_and_filter['reduced_reasons']
            },
            'applied_sort': sort_and_filter['applied_sort']
        }

        if request.GET.get('numprod'):
            request.session['num_products_per_page'] = request.GET.get(
                'numprod')
        elif ('num_products_per_page' not in request.session or
                not request.session['num_products_per_page']):
            request.session['num_products_per_page'] = 12

        context = apply_pagination(
            context,
            'products',
            request.GET.get('page', 1),
            request.session.get('num_products_per_page')
        )

        return render(request, 'products/products.html', context)

    return redirect(reverse('all_games'))


# Show all game product lines
def all_games(request):
    """
        A view to show all game product lines and redirect search queries,
        including sorting, filtering and pagination
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    sort_options = build_sort_options(
        ['name', 'category', 'genre', 'publisher'])

    context = {
        'sort_options': sort_options,
        'view': 'all_games',
        'products': Product_Line.objects.exclude(
            category__identifier='supplies'),
        'filters': [
            {
                'genres': Genre.objects.all().exclude(identifier='n_a').values(
                            'identifier', 'name').order_by('name'),
                'categories': Category.objects.all().exclude(
                    identifier='supplies').values(
                        'identifier', 'name').order_by('name'),
                'publishers': Publisher.objects.all().values(
                    'identifier', 'name').order_by('name')
            }
        ],
        'applied_filters': {
            'count': None,
            'categories': None,
            'genres': None,
            'publishers': None
        },
        'applied_sort': 'None_None'
    }

    if request.GET:
        sort_and_filter = apply_sort_and_filters(
            context['products'], request, 'all_games')

        context.update({
            'products': sort_and_filter['dataset'],
            'applied_filters': {
                'count': sort_and_filter['filter_count'],
                'categories': sort_and_filter['categories'],
                'genres': sort_and_filter['genres'],
                'publishers': sort_and_filter['publishers']
            },
            'applied_sort': sort_and_filter['applied_sort']
        })
    else:
        sort = apply_sort(context['products'], request, 'all_games')
        context.update({
            'products': sort['dataset'],
            'applied_sort': sort['applied_sort']
        })

    if request.GET.get('numprod'):
        request.session['num_products_per_page'] = request.GET.get('numprod')
    elif ('num_products_per_page' not in request.session or
            not request.session['num_products_per_page']):
        request.session['num_products_per_page'] = 12

    context = apply_pagination(
        context,
        'products',
        request.GET.get('page', 1),
        request.session.get('num_products_per_page')
    )

    return render(request, 'products/products.html', context)


# Show all products for a given product line
def products(request, product_line_id):
    """
        A view to show all products within a line and redirect search queries,
        including sorting, filtering and pagination
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    sort_options = build_sort_options(
        ['name', 'price::lh', 'category'])

    product_line = get_object_or_404(Product_Line, pk=product_line_id)
    if product_line.hidden is True:
        raise Http404

    context = {
        'sort_options': sort_options,
        'view': 'products',
        'product_line': product_line,
        'products': Product.objects.filter(
            sub_product_line__product_line__id=product_line_id),
        'filters': [
            {
                'sub_product_lines': Sub_Product_Line.objects.filter(
                    product_line=product_line_id).exclude(hidden=True).exclude(
                        product_line__hidden=True).exclude(
                            core_set=True).exclude(scenics=True).values(
                                'identifier', 'name').order_by('name'),
                'core_sets': Sub_Product_Line.objects.exclude(
                    hidden=True).exclude(product_line__hidden=True).filter(
                        product_line=product_line_id).filter(
                            core_set=True).values(
                                'identifier', 'name').order_by('name'),
                'scenics': Sub_Product_Line.objects.exclude(
                    hidden=True).exclude(product_line__hidden=True).filter(
                            product_line=product_line_id).filter(
                            scenics=True).values(
                                'identifier', 'name').order_by('name'),
            }
        ],
        'stock_states': Stock_State.objects.filter(
            id__in=Product.objects.filter(
                sub_product_line__product_line__id=product_line_id).values(
                    'stock_state_id').order_by(
                        'stock_state_id').distinct()).exclude(
                            identifier='no_longer_available').values(
                                'identifier', 'state').order_by('state'),
        'reduced_reasons': Reduced_Reason.objects.filter(
            id__in=Product.objects.filter(
                sub_product_line__product_line__id=product_line_id).values(
                    'reduced_reason_id').order_by(
                        'reduced_reason_id').distinct()).values(
                            'identifier', 'reason').order_by('reason'),
        'applied_filters': {
            'count': None,
            'categories': None,
            'stock': None,
            'reduced_reasons': None
        },
        'applied_sort': 'None_None'
    }

    if request.GET:
        sort_and_filter = apply_sort_and_filters(context['products'], request)

        context.update({
            'products': sort_and_filter['dataset'],
            'applied_filters': {
                'count': sort_and_filter['filter_count'],
                'categories': sort_and_filter['categories'],
                'stock': sort_and_filter['stock'],
                'reduced_reasons': sort_and_filter['reduced_reasons']
            },
            'applied_sort': sort_and_filter['applied_sort']
        })
    else:
        sort = apply_sort(context['products'], request)
        context.update({
            'products': sort['dataset'],
            'applied_sort': sort['applied_sort']
        })

    if request.GET.get('numprod'):
        request.session['num_products_per_page'] = request.GET.get('numprod')
    elif ('num_products_per_page' not in request.session or
            not request.session['num_products_per_page']):
        request.session['num_products_per_page'] = 12

    context = apply_pagination(
        context,
        'products',
        request.GET.get('page', 1),
        request.session.get('num_products_per_page')
    )

    return render(request, 'products/products.html', context)


# Show details of a given product
def product_detail(request, product_id):
    """
        A view to show products details and redirect search queries
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    products = adjust_max_per_purchase(Product.objects.filter(id=product_id))

    for product in products:
        if is_product_hidden(product) is True:
            product = set_product_instance_unavailable(product)

    context = {
        'view': 'product_detail',
        'products': products,
    }

    return render(request, 'products/product_detail.html', context)


# Perform a simple lookup based on a provided type key indicating the table to
# be queried
@login_required
@require_POST
def get_lookup(request, lookup_type):
    """
        Take a keyword from a request from an admin page, get a matching
        config object, and use that to run a lookup query and return results.

        This view is restricted to POST requests from staff accounts.
    """
    if not request.user.is_staff:
        raise PermissionDenied

    # Define the lookups object
    lookups = {
        'category': {
            'single': 'Category',
            'plural': 'Categories',
            'table': Category,
        },
        'genre': {
            'single': 'Genre',
            'table': Genre,
            'exclude': {
                'identifier': 'n_a'
            }
        },
        'publisher': {
            'single': 'Publisher',
            'table': Publisher,
        },
        'product_line': {
            'single': 'Product Line',
            'table': Product_Line,
            'extra_fields': [
                'hidden'
            ]
        },
        'product': {
            'single': 'Product',
            'table': Product,
            'filter_name': 'Sub Product Line',
            'filter_key': 'sub_product_line',
            'filter_val': request.POST.get('sub_product_line'),
            'skip_no_filter': False,
            'extra_fields': [
                'hidden'
            ],
            'error_name_extra': 'for this Sub Product Line',
            'error_error_extra': 'for this Sub Product Line'
        },
        'reduced_reason': {
            'single': 'Reduced Reason',
            'table': Reduced_Reason,
            'alt_name': 'reason',
            'extra_fields': [
                'default_reduction_percentage'
            ]
        },
        'stock_state': {
            'single': 'Stock State',
            'table': Stock_State,
            'alt_name': 'state',
            'exclude': {
                'identifier': 'no_longer_available'
            }
        },
        'sub_product_line': {
            'single': 'Sub Product Line',
            'table': Sub_Product_Line,
            'filter_name': 'Product Line',
            'filter_key': 'product_line',
            'filter_val': request.POST.get('product_line'),
            'skip_no_filter': True,
            'extra_fields': [
                'hidden'
            ],
            'error_name_extra': 'for this Product Line',
            'error_error_extra': 'for this Product Line'
        }
    }

    # Get the lookup object associated with the provided lookup type
    lookup = lookups.get(lookup_type)

    # if the lookup type is not found...
    if not lookup:
        # Get a list of valid lookup types
        validOptions = []
        for key in lookups.keys():
            validOptions.append(key)
        # define the lookup_vals object with the error details
        lookup_vals = [{
            'id': '-1',
            'name': f'No lookup available for {lookup_type}',
            'error': f'Please reformat your request and try again.  Valid \
                options: {validOptions}'
        }]

        # return the error
        return JsonResponse(lookup_vals, safe=False)

    # by default, do not apply a filter.
    use_filter = False

    # by default, if use filter is true, return an error if the filter is not
    # provided
    skip_no_filter = False

    # If the skip_no_filter key is present in the lookup, use that value
    if 'skip_no_filter' in lookup and lookup['skip_no_filter']:
        skip_no_filter = lookup['skip_no_filter']

    # If a filter key (field to filter by) is present, check for a filter value
    if 'filter_key' in lookup and lookup['filter_key']:
        # Set the filter name (used in messages) to the filter_key value
        filter_name = lookup['filter_key']

        # if a friendly name is provided for the filter, use that instead
        if 'filter_name' in lookup and lookup['filter_name']:
            filter_name = lookup['filter_name']

        # define the lookup_vals object anticipating an error
        lookup_vals = [{
            'id': '-1',
            'name': f'No {filter_name} or invalid {filter_name} supplied',
            'error': 'Please refresh the page and try again.'
        }]

        # If the filter value is present, set use_filter to true
        if 'filter_val' in lookup and lookup['filter_val']:
            use_filter = True

        # If the filter value is not present, and skip_no_filter is false,
        # return the error
        if use_filter is False and skip_no_filter is False:
            return JsonResponse(lookup_vals, safe=False)

    # by default we expect to return two columns - id, and name
    lookup_name = 'name'

    # If an alternative to name is provided in the lookup, use that instead
    if 'alt_name' in lookup and lookup['alt_name']:
        lookup_name = lookup['alt_name']

    lookup_fields = [
        'id',
        lookup_name
    ]

    # If the lookup specifies any additional fields, add them to lookup_fields
    if 'extra_fields' in lookup and lookup['extra_fields']:
        lookup_fields += lookup['extra_fields']

    # if we are using a filter...
    if use_filter is True:
        try:
            # convert the filter vals into a list incase more than one was
            # supplied
            lookup['filter_val'] = str(lookup['filter_val']).split(',')
            # filter the requested table by applying the filter val list to
            # the filter key (representing the field to filter by), and return
            # the values from the fields specified in the lookup_fields list
            lookup_vals = lookup['table'].objects.filter(
                    **{f'{lookup["filter_key"]}__in': lookup['filter_val']}
            ).values(*lookup_fields)

        except ValueError as e:
            # otherwise there was an error with one or more of the provided
            # filter values, so get the error string and update the
            # error key of the lookup_vals object we defined earlier
            lookup_vals[0]['error'] = str(e)
            # return the error
            return JsonResponse(lookup_vals, safe=False)

    # No filter, so get all objects from the table specified in the lookup, and
    # return the values from the fields specified in the lookup_fields list
    else:
        lookup_vals = lookup['table'].objects.all().values(*lookup_fields)

    # If the 'exclude' key is present in the lookup, apply it as an exclude to
    # the lookup_vals query set
    if 'exclude' in lookup and lookup['exclude']:
        lookup_vals = lookup_vals.exclude(**lookup['exclude'])

    # If we are executing a sub_product_line lookup, ensure that hidden is
    # set correctly for each result
    if lookup_type == 'sub_product_line':
        for sub_product_line in lookup_vals:
            if is_sub_product_line_hidden(sub_product_line) is True:
                sub_product_line['hidden'] = True
    # If we are executing a product lookup, ensure that hidden is set correctly
    # for each result
    elif lookup_type == 'product':
        for product in lookup_vals:
            if is_product_hidden(product) is True:
                product['hidden'] = True

    # Convert the queryset to a list for further processing
    lookup_vals = list(lookup_vals)

    # Pluralisation for messages
    # by default, suffix an 's' to the value of the 'single' key of the lookup.
    # Alternatively, use the 'plural' key if it is provided
    lookup_plural = lookup['single'] + 's'
    if 'plural' in lookup and lookup['plural']:
        lookup_plural = lookup['plural']

    # if our lookup returned no results...
    if len(lookup_vals) < 1:
        # redefine the lookup_vals object with an error message
        lookup_vals = [{
            'id': '-1',
            'name': f'No {lookup_plural} found',
            'error': f'Please create at least 1 {lookup["single"]}'
        }]
        # if the error_name_extra key exists in the lookup, append the value to
        # to the name key of our error response
        if 'error_name_extra' in lookup and lookup['error_name_extra']:
            lookup_vals[0]['name'] += ' ' + lookup['error_name_extra']

        # if the error_error_extra key exists in the lookup, append the value
        # to the error key of our error response
        if 'error_error_extra' in lookup and lookup['error_error_extra']:
            lookup_vals[0]['error'] += ' ' + lookup['error_error_extra']

    # Otherwise we have results.  If 'alt_name' is present, substitute the
    # alt_name key from the results with 'name'.  (Prevents having to
    # handle variant data with client JS)
    elif 'alt_name' in lookup and lookup['alt_name']:
        for obj in lookup_vals:
            obj['name'] = obj.pop(f'{lookup_name}')

    # Return the results
    return JsonResponse(lookup_vals, safe=False)


# Main Product Admin Page
@login_required
def product_management(request):
    """
        A view to show the product management page and redirect search queries.

        Restricted to staff.
    """
    if not request.user.is_staff:
        raise PermissionDenied

    # Redirect search requests
    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    # Add the view name to the context
    context = {
        'view': 'product_management'
    }

    # Render the product management page, passing the context
    return render(request, 'products/product_management.html', context)


# Get the configuration object for an add/edit request
def get_request_config_obj(request, request_config_key, object_id=None):
    """
        Take a keyword from a request and return a configuration object.

        Called by the add/edit views, which are restricted to staff
        accounts.
    """
    # Define the request configuration objects
    request_config_objects = {
        'product_line': {
            'view': 'product_line',
            'friendly': 'product line',
            'context': 'product_line_form',
            'context_obj': 'product_line_id',
            'table': Product_Line,
            'form': Product_Line_Form,
            'html': 'product_line_admin'
        },
        'product': {
            'view': 'product',
            'friendly': 'product',
            'context': 'product_form',
            'context_extra': {
                'default_max_per_purchase': settings.DEFAULT_MAX_PER_PURCHASE
            },
            'invalid_context_extra': {
                'product_line': request.POST.get('product_line')
            },
            'context_obj': 'product_id',
            'table': Product,
            'form': Product_Form,
            'html': 'product_admin'
        },
        'sub_product_line': {
            'view': 'sub_product_line',
            'friendly': 'sub product line',
            'context': 'sub_product_line_form',
            'context_obj': 'sub_product_line_id',
            'table': Sub_Product_Line,
            'form': Sub_Product_Line_Form,
            'html': 'sub_product_line_admin'
        },
        'category': {
            'view': 'category',
            'friendly': 'category',
            'context': 'category_form',
            'context_obj': 'category_id',
            'table': Category,
            'form': Category_Form,
            'html': 'category_admin'
        },
        'genre': {
            'view': 'genre',
            'friendly': 'genre',
            'context': 'genre_form',
            'context_obj': 'genre_id',
            'table': Genre,
            'form': Genre_Form,
            'html': 'genre_admin',
            'exclude': {
                'identifier': 'n_a'
            }
        },
        'publisher': {
            'view': 'publisher',
            'friendly': 'publisher',
            'context': 'publisher_form',
            'context_obj': 'publisher_id',
            'table': Publisher,
            'form': Publisher_Form,
            'html': 'publisher_admin'
        },
        'reduced_reason': {
            'view': 'reduced_reason',
            'friendly': 'reduced reason',
            'context': 'reduced_reason_form',
            'context_obj': 'reduced_reason_id',
            'table': Reduced_Reason,
            'form': Reduced_Reason_Form,
            'name': 'reason',
            'html': 'reduced_reason_admin'
        },
        'stock_state': {
            'view': 'stock_state',
            'friendly': 'stock state',
            'context': 'stock_state_form',
            'context_obj': 'stock_state_id',
            'table': Stock_State,
            'form': Stock_State_Form,
            'name': 'state',
            'html': 'stock_state_admin',
            'exclude': {
                'identifier': 'no_longer_available'
            }
        },
    }

    # Get the request config object associated with the provided request config
    # key
    request_config_obj = request_config_objects.get(request_config_key)

    # If no object was found, return None
    if request_config_obj is None:
        return None

    # If an object_id was provided (this is an edit request)...
    if object_id:
        # If the request config key was 'product'...
        if request_config_key == 'product' and object_id:
            # locate a product using the object id
            product = get_object_or_404(Product, id=object_id)
            # add the price of the product to the 'context_extra' key of the
            # request config object
            request_config_obj['context_extra']['product_price'] = (
                product.get_price())
            # add the id of the product line associated with the product to the
            # 'context_extra' key of the request config object
            request_config_obj['context_extra']['product_line'] = (
                product.sub_product_line.product_line.id)

        # If the request config object contains the 'exclude' key, then we
        # should check if the user is trying to edit an excluded item, and if
        # so, prevent the edit
        if 'exclude' in request_config_obj and request_config_obj['exclude']:
            # Filter the table from the request_config_obj for excluded items,
            # then filter again to determine if the item associated with the
            # object_id is returned
            excluded_item = request_config_obj['table'].objects.filter(
                **request_config_obj['exclude']).filter(id=object_id)

            # If excluded_item contains a result, then the user is attempting
            # edit an excluded item, so return none
            if len(excluded_item) > 0:
                return None

    # return the request config obj
    return request_config_obj


# Open the management page for a provided request config key to allow the
# staff user to add a new item to the DB
@login_required
def add(request, request_config_key):
    """
        A view to show the management page for the provided request config key,
        which allows a staff user to create a new item of the appropriate type

        Also redirects search request

        This view is restricted to staff
    """
    if not request.user.is_staff:
        raise PermissionDenied

    # Redirect search requests
    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    # Get the config object associated with the provided request_config_key
    config_obj = get_request_config_obj(request, request_config_key)

    # If no key is returned, raise a 404 error
    if config_obj is None:
        raise Http404

    # Create the view key in the context.  For example:
    #   add_product
    view = 'add_' + config_obj['view']
    context = {
        'view': view
    }

    # If the context_extra key is present in the config object, merge it into
    # the context
    if 'context_extra' in config_obj and config_obj['context_extra']:
        context |= config_obj['context_extra']

    # If this is a POST request...
    if request.method == 'POST':
        # retrieve the form from the config object, passing the POST and FILES
        # data
        form = config_obj['form'](request.POST, request.FILES)
        # If the form is valid...
        if form.is_valid():
            # Save the form
            result = form.save()
            # We need the correct field value for the success message, so
            # check the view key of the config object and define
            # added_item appropriately
            if config_obj['view'] == 'stock_state':
                added_item = result.state
            elif config_obj['view'] == 'reduced_reason':
                added_item = result.reason
            else:
                added_item = result.name
            # Send a success message utilising added_item
            messages.success(
                request,
                f'Successfully added {added_item}.',
                f'from__{view}_profile'
            )
            # redirect to the product_management page
            return redirect(reverse('product_management'))

        # If the form was invalid...
        else:
            # If the config object contains the 'invalid_context_extra' key,
            # merge it into the context
            if ('invalid_context_extra' in config_obj and
                    config_obj['invalid_context_extra']):
                context |= config_obj['invalid_context_extra']

            # Send an error message utilising the 'friendly' key of the config
            # object and do *not* redirect - we will reload the page below
            messages.error(
                request,
                f'Failed to add {config_obj["friendly"]}. Please ensure the \
                    form is valid.',
                f'from__{view}_profile'
            )

    # Otherwise this is a GET request, so retrieve the form from the config
    # object
    else:
        form = config_obj['form']()

    # Add the form to the context using the key name specified in the
    # config object
    context[config_obj['context']] = form

    # Render the admin page specified in the config object, passing the context
    return render(request, f'products/{config_obj["html"]}.html', context)


# Open the management page for a provided request config key to allow the
# staff user to edit an existing item in the DB (specified by the provided
# object_id)
@login_required
def edit(request, request_config_key, object_id):
    """
        A view to show the management page for the provided request config key,
        which allows a staff user to edit the item specified by the object_id

        Also redirects search request

        This view is restricted to staff
    """
    if not request.user.is_staff:
        raise PermissionDenied

    # Redirect search requests
    if request.GET:
        if 'q' in request.GET:
            return redirect(get_search_request(request))

    # Get the config object associated with the provided request_config_key
    config_obj = get_request_config_obj(request, request_config_key, object_id)

    # If no key is returned, raise a 404 error
    if config_obj is None:
        raise Http404

    # Get the item associated with the provided object_id
    item = get_object_or_404(config_obj['table'], id=object_id)

    # Create the view key in the context.  For example:
    #   edit_product
    view = 'edit_' + config_obj['view']
    context = {
        'view': view,
        # Add a key named for the context_obj key of the config
        # object, and add the object_id as it's value
        config_obj['context_obj']: object_id
    }

    # If the context_extra key is present in the config object, merge it into
    # the context
    if 'context_extra' in config_obj and config_obj['context_extra']:
        context |= config_obj['context_extra']

    # If this is a POST request...
    if request.method == 'POST':
        # retrieve the form from the config object, passing the POST and FILES
        # data, and setting the instance to the item
        form = config_obj['form'](request.POST, request.FILES, instance=item)
        # If the form is valid...
        if form.is_valid():
            # Save the form
            form.save()
            # We need the correct field value for the success message, so
            # check the view key of the config object and define
            # updated_item appropriately
            if config_obj['view'] == 'stock_state':
                updated_item = item.state
            elif config_obj['view'] == 'reduced_reason':
                updated_item = item.reason
            else:
                updated_item = item.name
            # Send a success message utilising updated_item
            messages.success(
                request,
                f'Successfully updated {updated_item}.',
                f'from__{view}_profile'
            )
            # redirect to the product_management page
            return redirect(reverse('product_management'))

        # If the form was invalid...
        else:
            # If the config object contains the 'invalid_context_extra' key,
            # merge it into the context
            if ('invalid_context_extra' in config_obj and
                    config_obj['invalid_context_extra']):
                context |= config_obj['invalid_context_extra']

            # Send an error message utilising the 'friendly' key of the config
            # object and do *not* redirect - we will reload the page below
            messages.error(
                request,
                f'Failed to save {config_obj["friendly"]} changes. Please \
                    ensure the form is valid.',
                f'from__{view}_profile'
            )

    # Otherwise this is a GET request, so retrieve the form from the config
    # object
    else:
        form = config_obj['form'](instance=item)

    # Add the form to the context using the key name specified in the
    # config object
    context[config_obj['context']] = form

    # Render the admin page specified in the config object, passing the context
    return render(request, f'products/{config_obj["html"]}.html', context)
