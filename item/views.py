from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from item.forms import ItemCreateForm
from item.models import Item, Offer, Condition
from django.contrib.auth.decorators import login_required

from messaging.models import Message


def catalog(request):
    if request.method == 'POST':
        search_list = request.POST.get('search').lower().split()
        conditions = Condition.objects.all()
        search_condition = None
        for condition in conditions:
            cur_condition = condition.name.lower().split()
            length = len(cur_condition)
            for i in range(len(search_list) - (length - 1)):
                if search_list[i:i+length] == cur_condition:
                    search_condition = condition
                    for item in cur_condition:
                        search_list.remove(item)
                    break
        search_string = ' '.join(search_list)
        context = {'items': Item.objects.filter(name__icontains=search_string, condition=search_condition)}
    else:
        context = {'items': Item.objects.all()}
    return render(request, 'item/catalog.html', context)


def get_item(request, id):
    context = {'item': get_object_or_404(Item, pk=id)}
    return render(request, 'item/get_item.html', context)


def get_category(request, category_id):
    context = {'items': Item.objects.filter(categories=category_id)}
    return render(request, 'item/catalog.html', context)


@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemCreateForm(data=request.POST)
        if form.is_valid():

            item = form.save(commit=False)
            item.seller = request.user
            item.save()
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
        message = Message(sender=request.user, receiver=offer.item.seller, subject='Nýtt tilboð í vöruna þína!', body=f'Þú átt nýtt tilboð í vöru: {offer.item.name} að upphæð {offer.amount}', related=offer)
        message.save()
    return redirect('item:get_item', id)


@login_required
def get_all_sales(request):
    pass


@login_required
def get_sale(request, id):
    pass
