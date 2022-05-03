from django.shortcuts import render, get_object_or_404

from item.forms.item_form import ItemCreateForm
from item.models import Item
from django.contrib.auth.decorators import login_required


def catalog(request):
    context = {'items': Item.objects.all()}
    return render(request, 'item/catalog.html', context)


def get_item(request, id):
    context = {'item': get_object_or_404(Item, pk=id)}
    return render(request, 'item/get_item.html', context)


def get_category(request, category_id):
    pass

@login_required
def create_item(request):
    if request.method == 'POST':
        pass
    else:
        form = ItemCreateForm()
    return render(request, 'item/create_item.html', {
        'form': form
    })
