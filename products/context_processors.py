from .models import (Product_Line, Sub_Product_Line)


# Context Processor used to populate product nav dropdown menus
def pop_product_nav_menus(request):
    '''
        Return a lists of products by key categories.  Used to populate nav
        dropdown menus.
    '''
    # Tabletop + Skirmish games
    tabletop_games = Product_Line.objects.filter(
        category__identifier__in=['tabletop', 'skirmish']).order_by('name')
    # Card games
    card_games = Product_Line.objects.filter(
        category__identifier='card').order_by('name')
    # Brushes and paint
    brushes_and_paint = Sub_Product_Line.objects.filter(
        product_line__identifier='brushes_and_paint').order_by('name')
    # Glue, Scenics and Tools
    hobby_essentials = Sub_Product_Line.objects.filter(
            product_line__identifier='hobby_essentials').order_by('name')
    hobby_essentials_id = list(
        hobby_essentials.values(
            'product_line_id').distinct())[0]['product_line_id']

    return {
        'nav_menus': {
            'tabletop_games': tabletop_games,
            'card_games': card_games,
            'brushes_and_paint': brushes_and_paint,
            'hobby_essentials': hobby_essentials,
            'hobby_essentials_id': hobby_essentials_id
        }
    }
