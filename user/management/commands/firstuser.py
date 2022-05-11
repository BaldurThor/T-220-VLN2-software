import os

from django.core.files import File
from django.core.management.base import BaseCommand

from django.conf import settings
from user.models import UserProfile
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User(username="thjarkurinn", first_name="Þjarkurinn", is_staff=True, is_superuser=True)
        user.set_password("admin")
        user.save()
        user_profile = UserProfile(user=user,
                                   avg_rating=10,
                                   bio='I was born at a very young age')
        with open(os.path.join(settings.BASE_DIR, 'static/images/robot.jpg'), 'rb') as f:
            user_profile.image.save('users/robot.jpg', File(f), save=True)