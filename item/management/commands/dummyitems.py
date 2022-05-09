import json
import os
from StringIO import StringIO

import requests

from django.conf import settings
from django.core.files import File
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from item.models import Item, Condition, Category
from user.models import Country


def getjsonobj(filename):
    data = open(filename, "r", encoding="utf8")
    return data


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = getjsonobj("dummyitems.json")
        dataclasses = json.load(data)
        objects = dataclasses.values()
        country = Country.objects.filter(name='Iceland').get()

        for i in objects:
            for e in i:
                e["condition"] = Condition.objects.get(name=e['condition'])
                e['zip'] = '600'
                e["country"] = country
                category_names = e.pop('categories')
                image_path = e.pop('image')
                item, created = Item.objects.get_or_create(**e)
                if created:
                    if image_path[0] == '/':
                        with open(os.path.join(settings.BASE_DIR, image_path), 'rb') as f:
                            file = File(f)
                    else:
                        r = requests.get(image_path)
                        f = StringIO(r.content)
                        file = File(f)
                    item.image.save(f'items/{os.path.basename(image_path)}', file)
                    categories = []
                    for category_name in category_names:
                        categories.append(Category.objects.get(name=category_name))
                    item.categories.set(categories)
                    item.save()


