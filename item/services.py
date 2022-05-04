from django.contrib.auth.models import User

from item.models import Offer
from messaging.models import Message


def offer_placed(offer):
    message = Message(sender=User.objects.get(pk=1),
                      receiver=offer.item.seller,
                      subject='Nýtt tilboð í vöruna þína!',
                      body=f'Þú átt nýtt tilboð í vöru: {offer.item.name} að upphæð {offer.amount}',
                      related=offer)
    message.save()


def offer_accepted(offer):
    other_offers = Offer.objects.filter(item=offer.item, pk__not=offer.id, rejected=False)
    for other_offer in other_offers:
        other_offer.rejected = True
        other_offer.save()
        offer_rejected(other_offer)


def offer_rejected(offer):
    pass
