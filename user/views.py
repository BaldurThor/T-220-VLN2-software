from django.shortcuts import render

# Create your views here.
from item.models import Item


def frontpage(request):
    context = {
        'items': Item.objects.order_by('?')[0:3]
    }
    return render(request, 'user/frontpage.html', context)


def register(request):
    pass
