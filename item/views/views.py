from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from user.models import Rating
from item.models import Item, Condition, Category, Sale
from item import filtering


class CatalogView(ListView):
    model = Item
    paginate_by = 24
    context_object_name = 'items'
    template_name = 'item/catalog.html'
    ORDERABLE = {
        "name": "Stafrófsröð",
        "-name": "Öfug stafrófsröð",
        "-views": "Mest Skoðað",
        "views": "Minnst Skoðað",
        "highest_offer": "Hæsta boð"
    }

    def get_queryset(self):
        queryset = Item.objects.filter(sold_at=None, is_deleted=False)
        queryset = filtering.apply_filter(self.request, queryset)
        order_by = self.request.GET.get('order_by')
        if order_by and order_by in self.ORDERABLE:
            if order_by == 'name':
                order_by = Lower(order_by)
            elif order_by == '-name':
                order_by = Lower('name').desc()
            elif order_by == 'highest_offer':
                order_by = '-highest_offer__amount'
            queryset = queryset.order_by(order_by)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['conditions'] = Condition.objects.all()
        context['categories'] = Category.objects.all()
        context['orderable'] = self.ORDERABLE

        context['filter'] = filtering.get_context(self.request)
        context['order_by'] = self.request.GET.get('order_by')
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
