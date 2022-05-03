from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from item.forms import ItemCreateForm
from item.models import Item, Offer
from django.contrib.auth.decorators import login_required


def catalog(request):
    context = {'items': Item.objects.all()}
    return render(request, 'item/catalog.html', context)


def get_item(request, id):
    context = {'item': get_object_or_404(Item, pk=id)}
    return render(request, 'item/get_item.html', context)


def get_category(request, category_id):
    context = {'items': Item.objects.filter(categories=category_id)}
    return render(request, 'item/catalog.html', context)


def search(request, string):
    context = {'items': Item.objects.filter(name__icontains=string)}
    return render(request, 'item/catalog.html', context)


@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('item:catalog')
    else:
        form = ItemCreateForm()
    return render(request, 'item/create_item.html', {
        'form': form
    })


@login_required
def submit_offer(request, id):
    if request.method == 'POST' and request.POST.get('amount') != '':
        offer = Offer()
        offer.user = request.user
        offer.item = Item.objects.get(pk=id)
        offer.date = now()
        offer.amount = int(request.POST.get('amount'))
        offer.save()
    return redirect('item:get_item', id)


@login_required
def get_all_sales(request):
    pass


@login_required
def get_sale(request, id):
    pass
