from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma

from item.models import Offer, Item
from messaging.models import Message


def offer_placed(offer):
    message = Message(sender=User.objects.get(username=settings.FIRESALE_BOT_USERNAME),
                      receiver=offer.item.seller,
                      subject='Nýtt tilboð í vöruna þína!',
                      body=f'Þú átt nýtt tilboð í vöru: {offer.item.name} að upphæð {intcomma(offer.amount)}',
                      related=offer,
                      type='Offer_new',
                      )
    message.save()


def offer_accepted(offer):
    other_offers = Offer.objects.filter(item=offer.item, rejected=False).exclude(pk=offer.id)
    for other_offer in other_offers:
        other_offer.rejected = True
        other_offer.save()
        offer_rejected(other_offer)

    message = Message(sender=User.objects.get(username=settings.FIRESALE_BOT_USERNAME),
                      receiver=offer.user,
                      subject=f'🎉🎉🎉Tilboðið þitt í {offer.item.name} er samþykkt!🎉🎉🎉',
                      body=f'Tilboðið þitt í {offer.item.name} hefur verið samþykkt. upplýsingarnar eru hægra megin,\nendilega farðu yfir að allt sé rétt.\nÝttu á ganga frá kaupum til að klára kaupin.',
                      related=offer,
                      type='Offer_accepted',
                      )
    message.save()


def offer_rejected(offer):
    message = Message(sender=User.objects.get(username=settings.FIRESALE_BOT_USERNAME),
                      receiver=offer.user,
                      subject=f'Tilboði þínu í {offer.item.name} hefur verið hafnað.',
                      related=offer,
                      type='Offer_rejected',
                      )
    message.save()


def sale_completed(sale):
    message = Message(sender=User.objects.get(username=settings.FIRESALE_BOT_USERNAME),
                      receiver=sale.buyer,
                      subject=f'Takk fyrir kaupinn á {sale.item.name}',
                      body=f'Kaupinn þín á {sale.item.name} eru kláruð,\nog {intcomma(sale.amount)} kr. hafa verið gjaldfærð á kortið "{sale.card_name}, {sale.card_number[-4:]}"',
                      related=sale,
                      type='Sale_completed',
                      )
    message.save()


def get_similar(o_item):
    return_list = []
    for _ in range(3):
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
