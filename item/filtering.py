import operator
from functools import reduce
import re

from django.db.models import Q


def filter_queryset(queryset, search_string, model, related_name, fields=None):
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
