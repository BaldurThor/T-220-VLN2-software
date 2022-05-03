from django.shortcuts import render

# Create your views here.
from item.models import Item


def frontpage(request):
    context = {'items': Item.objects.all()}
    return render(request, 'user/frontpage.html', context)

def get_random_items():
    pass