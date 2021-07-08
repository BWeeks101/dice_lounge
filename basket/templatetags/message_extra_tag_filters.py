from django import template


register = template.Library()


@register.filter(name='get_product_id')
def get_product_id(extra_tags):
    taglist = extra_tags.split(',')
    for tag in taglist:
        if tag.startswith('id_'):
            product_id = int(tag.replace('id_', ''))
            return product_id
    return None


@register.filter(name='get_sender')
def get_sender(extra_tags):
    taglist = extra_tags.split(',')
    for tag in taglist:
        if tag.startswith('sender_'):
            product_id = tag.replace('sender_', '')
            return product_id
    return None
