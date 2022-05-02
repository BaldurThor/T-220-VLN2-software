from django.core.management.base import BaseCommand
from item.models import Category, Condition


conditions = [
    'Factory New',
    'Minimal Wear',
    'Field Tested',
    'Well Worn',
    'Battle Scarred',
]

categories = [
    'Dekk',
    'Hnífar',
    'Rakettur',
    'Kveikjarar',
    'Steinar',
    'Brauð',
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for condition_name in conditions:
            condition, created = Condition.objects.get_or_create(name=condition_name)
            if created:
                condition.save()

        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                category.save()
