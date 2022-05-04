from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from . import services
from item.forms import ItemCreateForm
from item.models import Item, Offer, Condition, Category
from django.contrib.auth.decorators import login_required
from messaging.models import Message


def catalog(request):
    if request.method == 'POST':
        search_list = request.POST.get('search').lower().split()
        filter = {}

        conditions = Condition.objects.all()
        search_list, search_condition = con_cat_for(search_list, conditions)
        if search_condition:
            filter['condition'] = search_condition

        categories = Category.objects.all()
        search_list, search_category = con_cat_for(search_list, categories)
        if search_category:
            filter['categories'] = search_category
        filter['name__icontains'] = ' '.join(search_list)
        items = Item.objects.filter(**filter)

    else:
        items = Item.objects.filter(sold_at=None)
    context = {'items': items}
    return render(request, 'item/catalog.html', context)


def con_cat_for(lis1, lis2):
    return_object = None
    for item in lis2:
        cur_item = item.name.lower().split()
        length = len(cur_item)
        for i in range(len(lis1) - (length - 1)):
            if lis1[i:i + length] == cur_item:
                return_object = item
                for rem_item in cur_item:
                    lis1.remove(rem_item)
                break
    return lis1, return_object


def get_item(request, id):
    item = get_object_or_404(Item, pk=id)
    item.views += 1
    item.save()
    context = {'item': item}
    return render(request, 'item/get_item.html', context)


def get_category(request, category_id):
    item = Item.objects.filter(categories=category_id, sold_at=None)
    context = {'items': item}
    return render(request, 'item/catalog.html', context)


@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemCreateForm(data=request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            values = request.POST.getlist('categories')
            for value in values:
                item.categories.add(Category.objects.get(pk=value))
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
        services.offer_placed(offer)
    return redirect('item:get_item', id)


@login_required
def accept_offer(request, offer_id):
    offer = Offer.objects.get(pk=offer_id, item__seller=request.user)
    context = {
        'offer': offer
    }
    if request.method == 'POST':
        offer.accepted = True
        offer.item.accepted_offer = offer
        offer.item.sold_at = now()
        offer.save()
        offer.item.save()
        services.offer_accepted(offer)
        return redirect('item:get_all_offers')

    return render(request, 'item/accept_offer.html', context)


@login_required
def reject_offer(request, offer_id):
    offer = Offer.objects.get(pk=offer_id, item__seller=request.user)
    context = {
        'offer': offer
    }
    if request.method == 'POST':
        offer.rejected = True
        offer.save()
        services.offer_rejected(offer)
        return redirect('item:get_all_offers')

    return render(request, 'item/reject_offer.html', context)


@login_required
def get_all_offers(request):
    own_offers = Offer.objects.filter(
        user=request.user,
        rejected=False
    )
    other_offers = Offer.objects.filter(
        item__seller=request.user,
        rejected=False,
        accepted=False
    )
    context = {'own_offers': own_offers, 'other_offers': other_offers}
    return render(request, 'item/get_all_offers.html', context)


@login_required
def get_all_sales(request):
    pass


@login_required
def get_sale(request, id):
    pass


@login_required
def checkout(request, offer_id):
    offer = Offer.objects.get(pk=offer_id, accepted=True)
    context = {
        'offer': offer,
    }
    return render(request, 'item/checkout.html', context)
