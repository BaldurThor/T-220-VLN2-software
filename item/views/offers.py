from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.timezone import now

from item import services
from item.forms import SubmitOfferForm
from item.models import Offer


@login_required
def submit_offer(request):
    if request.method == 'POST':
        form = SubmitOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
            services.offer_placed(offer)
            messages.add_message(request, messages.SUCCESS, 'Tilboð er móttekið.')
        else:
            messages.add_message(request, messages.ERROR, form.errors)
        print(form.cleaned_data)
        if item := form.cleaned_data.get('item'):
            return redirect('item:get_item', item.id)
        else:
            return redirect('frontpage')
    raise Http404()


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
        rejected=False,
        sale=None,
    )
    other_offers = Offer.objects.filter(
        item__seller=request.user,
        rejected=False,
        accepted=False,
        sale=None
    )
    context = {'own_offers': own_offers, 'other_offers': other_offers}
    return render(request, 'item/get_all_offers.html', context)
