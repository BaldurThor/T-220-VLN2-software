from django.contrib.auth.models import User
from django.http import HttpResponse

from item.models import Offer, Item
from messaging.models import Message

import random


def offer_placed(offer):
    message = Message(sender=User.objects.get(pk=1),
                      receiver=offer.item.seller,
                      subject='Nýtt tilboð í vöruna þína!',
                      body=f'Þú átt nýtt tilboð í vöru: {offer.item.name} að upphæð {offer.amount}',
                      related=offer,
                      type='New_offer',
                      )
    message.save()


def offer_accepted(offer):
    other_offers = Offer.objects.filter(item=offer.item, rejected=False).exclude(pk=offer.id)
    for other_offer in other_offers:
        other_offer.rejected = True
        other_offer.save()
        offer_rejected(other_offer)

    message = Message(sender=User.objects.get(pk=1),
                      receiver=offer.user,
                      subject=f'🎉🎉🎉Tilboðið þitt í {offer.item.name} er samþykkt! 🎉🎉🎉',
                      body=f'',
                      related=offer,
                      type='Offer_accepted',
                      )
    message.save()


def offer_rejected(offer):
    message = Message(sender=User.objects.get(pk=1),
                      receiver=offer.user,
                      subject=f'Tilboði þínu í {offer.item.name} hefur verið hafnað.',
                      related=offer,
                      type='Offer_rejected',
                      )
    message.save()


def delete_item(item, user):
    if item.seller == user:
        item.is_deleted = True
        item.save()
        offers_on_item = Offer.objects.filter(item=item, rejected=False)
        for offer in offers_on_item:
            offer_rejected(offer)
    else:
        return HttpResponse('Unauthorized', status=401)


def get_similar(o_item):
    return_list = []
    for i in range(3):
        category = o_item.categories.order_by('?')[0]
        pk_exclude = [o.id for o in [o_item] + return_list]
        try:
            item = Item.objects.order_by('?').filter(sold_at=None, categories=category).exclude(pk__in=pk_exclude)[0]
            return_list.append(item)
        except IndexError:
            pass
    if return_list:
        return return_list
    return None
