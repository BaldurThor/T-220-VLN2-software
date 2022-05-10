import operator
from functools import reduce
import re

from django.db.models import Q

from item.models import Condition, Category


def filter_search_queryset(queryset, search_string, model, related_name, fields=None):
    if not fields:
        fields = ['name']
    search_words = search_string.split()
    filters = []
    for field in fields:
        for word in search_words:
            filters.append(Q(**{f'{field}__icontains': word}))
    rows = model.objects.filter(reduce(operator.or_, filters))
    if rows:
        queryset = queryset.filter(**{f'{related_name}__pk__in': rows})
    return queryset, rows


def strip_search_string(search_string, rows, fields=None):
    if not fields:
        fields = ['name']
    for row in rows:
        for field in fields:
            for w in getattr(row, field).lower().split():
                search_string = search_string.replace(w, '')
    search_string = re.sub(' +', ' ', search_string.strip())
    return search_string


def apply_filter(request, queryset):
    if condition_id := request.GET.get('condition', False):
        if condition_id.isnumeric():
            queryset = queryset.filter(condition__pk=condition_id)

    if categories := request.GET.getlist('categories'):
        queryset = queryset.filter(categories__in=categories)
    return queryset


def get_context(request):
    context = {
        'condition': request.GET.get('condition', ''),
        'categories': request.GET.getlist('categories'),
        'condition_obj': None,
        'categories_obj': None,
    }
    if context['condition'].isnumeric():
        try:
            context['condition_obj'] = Condition.objects.get(pk=context['condition'])
        except Condition.DoesNotExist:
            context['condition_obj'] = None

    context['categories_obj'] = Category.objects.filter(pk__in=context.get('categories'))

    return context
