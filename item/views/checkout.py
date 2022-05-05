from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from item.models import Offer


@login_required
def checkout(request, offer_id):
    offer = Offer.objects.get(pk=offer_id, accepted=True)
    context = {
        'offer': offer,
    }
    return render(request, 'item/checkout.html', context)
