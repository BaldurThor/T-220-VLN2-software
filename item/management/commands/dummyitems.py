import json
from django.core.management.base import BaseCommand
from item.models import Item, Condition
from user.models import Country


def getjsonobj(filename):
    data = open(filename, "r", encoding="utf8")
    return data


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = getjsonobj("dummyitems.json")
        dataclasses = json.load(data)
        objects = dataclasses.values()
        condition = Condition.objects.filter(name='Factory New').get()
        country = Country.objects.filter(name='Iceland').get()

        for i in objects:
            for e in i:
                e["condition"] = condition
                e["country"] = country
                item, created = Item.objects.get_or_create(**e)
                if created:
                    item.save()


