from django.conf import settings
from django.contrib.auth.models import User
from .models import Message


def notify(receiver, subject, body):
    sender = User.objects.get(username=settings.FIRESALE_BOT_USERNAME)
    message = Message(sender=sender, receiver=receiver, subject=subject, body=body)
    message.save()
