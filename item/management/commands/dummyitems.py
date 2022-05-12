import json
import os
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from item.models import Item, Condition, Category, ItemImage
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
                    image_path_list = image_path.split('.')
                    banner_path = image_path_list[0] + 'banner.' + image_path_list[1]
                    card_path = image_path_list[0] + 'card.' + image_path_list[1]
                    with open(os.path.join(settings.BASE_DIR, card_path), 'rb') as f:
                        file = File(f)
                        item.image.save(f'{os.path.basename(card_path)}', file)
                    with open(os.path.join(settings.BASE_DIR, banner_path), 'rb') as f:
                        file = File(f)
                        item.banner.save(f'{os.path.basename(banner_path)}', file)
                    with open(os.path.join(settings.BASE_DIR, image_path), 'rb') as f:
                        image = ItemImage(item=item, alt=image_path_list[0])
                        file = File(f)
                        image.image.save(f'{os.path.basename(image_path)}', file)

                    categories = []
                    for category_name in category_names:
                        categories.append(Category.objects.get(name=category_name))
                    item.categories.set(categories)
                    item.save()


