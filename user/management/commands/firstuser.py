from django.core.management.base import BaseCommand
from user.models import UserProfile
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User(username="thjarkurinn", first_name="Þjarkurinn", is_staff=True, is_superuser=True)
        user.set_password("admin")
        user.save()
        user_profile = UserProfile(user=user,
                                   avg_rating=10,
                                   image_url='https://luxai.com/wp-content/uploads/2020/11/QTrobot_exprssive-humanoid-robot-for-research.png',
                                   bio='I was born at a very young age')
        user_profile.save()
