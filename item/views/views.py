import operator
from functools import reduce
import re

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from item.services import delete_item
from user.models import UserProfile, Rating, Country
from item import services
from item.forms import ItemCreateForm
from item.models import Item, Offer, Condition, Category, Sale
from django.contrib.auth.decorators import login_required

from item import filtering


class CatalogView(ListView):
    model = Item
    paginate_by = 24
    context_object_name = 'items'
    template_name = 'item/catalog.html'

    def get_queryset(self):
        queryset = Item.objects.filter(sold_at=None, is_deleted=False)
        queryset = filtering.apply_filter(self.request, queryset)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['conditions'] = Condition.objects.all()
        context['categories'] = Category.objects.all()

        context['filter'] = filtering.get_context(self.request)
        return context


class SearchView(CatalogView):
    def get_queryset(self):
        search_string = self.request.GET.get('search', '').lower()
        queryset = super().get_queryset()

        if search_string:
            queryset, categories = filtering.filter_search_queryset(queryset, search_string, Category, 'categories')
            queryset, conditions = filtering.filter_search_queryset(queryset, search_string, Condition, 'condition')

            search_string = filtering.strip_search_string(search_string, categories)
            search_string = filtering.strip_search_string(search_string, conditions)

        if search_string:
            queryset = queryset.filter(name__icontains=search_string)
        return queryset


def get_item(request, id):
    item = get_object_or_404(Item, pk=id)
    if request.method == 'POST':
        delete_item(item, request.user)
    else:
        view_session = request.session.get('viewed_items', [])
        if item.id not in view_session:
            item.views += 1
            item.save()
            view_session.append(item.id)
            request.session['viewed_items'] = view_session
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


@login_required
def create_item(request):
    categories_choices = Category.objects.values_list('id', 'name')

    if request.method == 'POST':
        form = ItemCreateForm(request.POST, request.FILES, categories_choices=categories_choices)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            values = request.POST.getlist('categories')
            item.categories.add(*values)

            messages.add_message(request, messages.SUCCESS, 'Varan hefur verið stofnuð.')
            return redirect('item:catalog')
    else:
        item = Item()
        try:
            item.country = Country.objects.get(name='Iceland')
        except Country.DoesNotExist:
            pass
        form = ItemCreateForm(
            instance=item,
            categories_choices=categories_choices
        )
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
    try:
        rating = Rating.objects.get(rater=request.user, rated=sale.seller)
    except Rating.DoesNotExist:
        rating = None
    return render(request, 'item/get_sale.html', {
        'sale': sale,
        'rating': rating,
    })
