import json
import os

from django.core.files import File
from django.core.management.base import BaseCommand

from django.conf import settings
from user.models import UserProfile
from django.contrib.auth.models import User


def getjsonobj(filename):
    data = open(filename, "r", encoding="utf8")
    return data


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = getjsonobj("dummyusers.json")
        dataclasses = json.load(data)
        objects = dataclasses.values()
        for i in objects:
            for e in i:
                username = e['first_name'] + e['last_name'][0]
                user = User(
                    username=username,
                    first_name=e['first_name'],
                    last_name=e['last_name'],
                )
                user.set_password("generic")
                user.save()
                user_profile = UserProfile(
                    user=user,
                    bio=e['bio']
                )
                with open(os.path.join(settings.BASE_DIR, e['image']), 'rb') as f:
                    user_profile.image.save(f'users/{e["image"].split("/")[-1]}', File(f), save=True)
