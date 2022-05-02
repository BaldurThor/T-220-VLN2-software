from django import forms

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_receiver(receiver):
    if not User.objects.filter(username=receiver).exists():
        raise ValidationError('Notandanafn er ekki til.')


class MessageForm(forms.Form):
    receiver = forms.CharField(validators=[validate_receiver])
    subject = forms.CharField(min_length=3)
    body = forms.CharField(widget=forms.Textarea)
