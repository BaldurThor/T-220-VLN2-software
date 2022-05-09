from django import template
register = template.Library()


@register.simple_tag(takes_context=True)
def pagination_qs(context, page):
    query_params = context['request'].GET.copy()
    query_params['page'] = page
    return '?' + query_params.urlencode()
