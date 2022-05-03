from django.shortcuts import render

# Create your views here.
from item.models import Item


def frontpage(request):
    context = get_random_items()
    return render(request, 'user/frontpage.html', context)


def get_random_items():
    item_object = list(Item.objects.all().order_by('?'))
    if len(item_object) > 2:
        item_object = item_object[0:3]
    context = {}
    for i, item in enumerate(item_object):
        context.update({f'item{i}': item})
    for i in range(len(context), 3):
        context.update({f'item{i}': item_object[-1]})
    return context
