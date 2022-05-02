from django.contrib.auth.models import User
from .models import Message


def notify(receiver, subject, body):
    sender = User.objects.get(pk=1)
    message = Message(sender=sender, receiver=receiver, subject=subject, body=body)
    message.save()


def notifyMany(receivers, subject, body):
    for receiver in receivers:
        notify(receiver, subject, body)

