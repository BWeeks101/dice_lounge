from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (Product_Line, Stock_State, Sub_Product_Line, Product,
                     Category, Genre, Publisher)

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
    '''
    queries = (Q(name__icontains=query) |
               Q(description__icontains=query) |
               Q(sub_product_line__name__icontains=query) |
               Q(sub_product_line__identifier__icontains=query) |
               Q(sub_product_line__product_line__name__icontains=query) |
               Q(sub_product_line__product_line__identifier__icontains=query) |
               Q(**{
                   'sub_product_line__product_line__publisher__name' +
                   '__icontains': query
                   }) |
               Q(**{
                   'sub_product_line__product_line__publisher__identifier' +
                   '__icontains': query
                   }))
    return Product.objects.filter(queries)


# Apply selected sort to dataset
def apply_sort(dataset, request, view=None):
    '''
        Apply specified sort to dataset and return it along with a generated
        sort key describing the sort field and direction
    '''

    sortkey = None
    direction = None

    if 'sort' in request.GET:
        sortkey = request.GET['sort']
    else:
        sortkey = 'name'

    sortkeys = {
        'name': 'lower_name',
        'price': 'price',
        'stock': 'stock_state__state',
        'product_line': 'sub_product_line__product_line__name',
        'genre': 'genre__identifier',
        'category': 'category__identifier',
        'publisher': 'publisher__identifier'
    }

    if view == 'search':
        sortkeys.update({
            'category': 'sub_product_line__name',
            'publisher': 'sub_product_line__product_line__publisher__name'
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
        'publisher': 'sub_product_line__product_line__publisher'
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
            categories = Sub_Product_Line.objects.filter(
                identifier__in=categories).values('identifier')

    if 'product_line' in request.GET:
        product_lines = request.GET['product_line'].split(',')
        filter_count += len(product_lines)
        dataset = dataset.filter(**{
            filters.get('product_line') + '__identifier__in': product_lines
        })
        product_lines = Product_Line.objects.filter(
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

    return {
        'dataset': dataset,
        'filter_count': filter_count,
        'stock': stock_states,
        'categories': categories,
        'product_lines': product_lines,
        'genres': genres,
        'publishers': publishers,
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


# Adjust max_per_purchase by stock
# NB: Converts a QuerySet into a List, and returns a List
def adjust_max_per_purchase(products):
    products = list(products)
    for product in products:
        if product.max_per_purchase > product.stock:
            product.max_per_purchase = product.stock

    return products


# Return search results
def search_results(request):
    """
        A view to show all products in a set of search results,
        including sorting and filtering
    """

    if request.GET:
        # Strip leading/trailing whitespace, then get up to 254 chars of the
        # query parameter
        query = request.GET['q'].strip()[:254]

        # If no query parameter, send a message and redirect
        if not query:
            messages.error(
                request,
                "You didn't enter any search criteria",
                'sender_search'
            )
            redirect_url = request.GET.get('redirect_url')
            if redirect_url is None:
                return redirect(reverse('all_games'))
            return redirect(redirect_url)

        # Apply the query to the Product table, then sort the results
        sort_and_filter = apply_sort(
            apply_query(query), request)

        # If no results, send a message and redirect
        if len(sort_and_filter['dataset']) == 0:
            messages.info(
                request,
                "No results found.  Please try another search term.",
                'sender_search'
            )
            redirect_url = request.GET.get('redirect_url')
            if redirect_url is None:
                return redirect(reverse('all_games'))
            return redirect(redirect_url)

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

        stock_states = Stock_State.objects.filter(
                id__in=sort_and_filter['dataset'].values(
                    'stock_state__id')).values('id').order_by(
                        'id').distinct().values(
                            'identifier', 'state').order_by('state')

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
            'search_term': query,
            'applied_filters': {
                'count': sort_and_filter['filter_count'],
                'categories': sort_and_filter['categories'],
                'product_lines': sort_and_filter['product_lines'],
                'publishers': sort_and_filter['publishers'],
                'stock': sort_and_filter['stock'],
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
        A view to show all game product lines,
        including sorting, and redirect search queries
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect(
                reverse('search_results') + '?q=' + request.GET['q'] +
                '&redirect_url=' + request.GET.get('redirect_url')
            )

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
        A view to show all products within a line,
        including sorting, and redirect search queries
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect(
                reverse('search_results') + '?q=' + request.GET['q'] +
                '&redirect_url=' + request.GET.get('redirect_url')
            )

    sort_options = build_sort_options(
        ['name', 'price::lh', 'category'])

    context = {
        'sort_options': sort_options,
        'view': 'products',
        'product_line': get_object_or_404(Product_Line, pk=product_line_id),
        'products': Product.objects.filter(
            sub_product_line__product_line__id=product_line_id),
        'filters': [
            {
                'sub_product_lines': Sub_Product_Line.objects.filter(
                    product_line=product_line_id).exclude(
                        core_set=True).exclude(scenics=True).values(
                            'identifier', 'name').order_by('name'),
                'core_sets': Sub_Product_Line.objects.filter(
                    product_line=product_line_id).filter(
                        core_set=True).values('identifier', 'name').order_by(
                            'name'),
                'scenics': Sub_Product_Line.objects.filter(
                    product_line=product_line_id).filter(
                        scenics=True).values('identifier', 'name').order_by(
                            'name'),
            }
        ],
        'stock_states': Stock_State.objects.filter(
            id__in=Product.objects.filter(
                sub_product_line__product_line__id=product_line_id).values(
                    'stock_state_id').order_by(
                        'stock_state_id').distinct()).values(
                            'identifier', 'state').order_by('state'),
        'applied_filters': {
            'count': None,
            'categories': None,
            'stock': None
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
                'stock': sort_and_filter['stock']
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
        A view to show products details
    """

    if request.GET:
        if 'q' in request.GET:
            return redirect(
                reverse('search_results') + '?q=' + request.GET['q'] +
                '&redirect_url=' + request.GET.get('redirect_url')
            )

    products = adjust_max_per_purchase(Product.objects.filter(id=product_id))

    context = {
        'view': 'product_detail',
        'products': products,
    }

    return render(request, 'products/product_detail.html', context)
