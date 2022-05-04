from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from item.forms import ItemCreateForm
from item.models import Item, Offer, Condition, Category
from django.contrib.auth.decorators import login_required
from messaging.models import Message


def catalog(request):
    if request.method == 'POST':
        search_list = request.POST.get('search').lower().split()
        conditions = Condition.objects.all()
        categories = Category.objects.all()
        search_list, search_condition = con_cat_for(search_list, conditions)
        search_list, search_category = con_cat_for(search_list, categories)
        search_string = ' '.join(search_list)

        if search_condition and search_category:
            items = Item.objects.filter(name__icontains=search_string, condition=search_condition, categories=search_category)

        elif search_category:
            items = Item.objects.filter(name__icontains=search_string, categories=search_category)

        elif search_condition:
            items = Item.objects.filter(name__icontains=search_string, condition=search_condition)

        else:
            items = Item.objects.filter(name__icontains=search_string)

        context = {'items': items}
    else:
        context = {'items': Item.objects.all()}
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
    item = Item.objects.filter(categories=category_id)
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
def accept_offer(request, offer_id):
    context = {}
    if request.method == 'POST':
        pass

    return render(request, 'item/accept_offer.html', context)


@login_required
def get_all_offers(request):
    own_offers = Offer.objects.filter(user=request.user)
    other_offers = Offer.objects.filter(
        item__seller=request.user
    )
    context = {'own_offers': own_offers, 'other_offers': other_offers}
    return render(request, 'item/get_all_offers.html', context)


@login_required
def get_offer(request, id):
    offer = get_object_or_404(Offer, pk=id)
    context = {'offer': offer}
    return render(request, 'item/get_offer.html', context)


@login_required
def get_all_sales(request):
    pass


@login_required
def get_sale(request, id):
    pass
