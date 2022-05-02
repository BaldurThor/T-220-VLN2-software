from django.core.management.base import BaseCommand
from user.models import Country


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('countries.csv') as f:
            for line in f.readlines():
                country, created = Country.objects.get_or_create(name=line.strip())
                if created:
                    country.save()

