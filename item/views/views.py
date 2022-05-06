from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from item.services import delete_item
from user.models import UserProfile
from item import services
from item.forms import ItemCreateForm
from item.models import Item, Offer, Condition, Category, Sale
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
        items = Item.objects.filter(sold_at=None, is_deleted=False)
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
    if request.method == 'POST':
        delete_item(item, request.user)
    else:
        item.views += 1
        item.save()
    seller = UserProfile.objects.get(user=item.seller)
    context = {'item': item, 'seller': seller}
    similar_items = services.get_similar(item)
    if similar_items:
        context['similar_items'] = similar_items
    try:
        offer = Offer.objects.order_by('-amount').filter(item=item, rejected=False)[0]
        context['offer'] = offer
    except ObjectDoesNotExist:
        pass
    except IndexError:
        pass
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
            item.categories.add(*values)
            return redirect('item:catalog')
    else:
        form = ItemCreateForm()
    return render(request, 'item/create_item.html', {
        'form': form
    })


@login_required
def get_all_sales(request):
    own_sales = Sale.objects.filter(
        seller=request.user
    )
    other_sales = Sale.objects.filter(
        buyer=request.user
    )
    context = {'own_sales': own_sales, 'other_sales': other_sales}
    return render(request, 'item/get_all_sales.html', context)


@login_required
def get_sale(request, sale_id):
    sale = Sale.objects.filter(pk=sale_id).filter(Q(seller=request.user) | Q(buyer=request.user)).get()
    return render(request, 'item/get_sale.html', {
        'sale': sale,
    })

