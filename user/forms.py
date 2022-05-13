from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from user.models import UserProfile
from django.forms.widgets import ClearableFileInput

from . import models


def validate_username(username):
    if User.objects.filter(username=username).exists():
        raise forms.ValidationError('Notandanafn er nú þegar til.')


def split_name(fullname):
    i = fullname.rfind(' ')
    if i:
        last_name = fullname[i+1:]
        first_name = fullname[:i].strip()
    else:
        last_name = ''
        first_name = fullname
    return first_name, last_name


class RegistrationForm(forms.Form):
    username = forms.CharField(validators=[validate_username], label='Notendanafn')
    email = forms.EmailField(label='Netfang')
    fullname = forms.CharField(label='Fullt nafn')
    password = forms.CharField(widget=forms.PasswordInput(), label='Lykilorð')
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Staðfesta lykilorð')

    def clean(self):
        super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError('Lykilorðin stemma ekki')
        self.cleaned_data.pop('password_confirm')
        password_validation.validate_password(self.cleaned_data['password'])
        self.cleaned_data['first_name'], self.cleaned_data['last_name'] = split_name(self.cleaned_data.pop('fullname'))


class UpdateProfileForm(forms.ModelForm):
    fullname = forms.CharField(label='Fullt nafn', required=False)
    image = forms.ImageField(label='Mynd', required=False)
    banner = forms.ImageField(label='Forsíðu mynd', required=False)

    class Meta:
        model = models.UserProfile
        fields = ['bio', 'image', 'banner']

    def clean(self):
        self.cleaned_data['first_name'], self.cleaned_data['last_name'] = split_name(self.cleaned_data.pop('fullname'))

    def clean_imagefield(self, field_name):
        image = self.cleaned_data.get(field_name, False)
        if image:
            if image.size > 10*1024*1024:
                raise forms.ValidationError('Mynd of stór! (> 10mb )')
            return image

    def clean_image(self):
        return self.clean_imagefield('image')

    def clean_banner(self):
        return self.clean_imagefield('banner')


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = ['full_name', 'country', 'street_name', 'house_number', 'city', 'zip']
        labels = {
            'full_name': 'Fullt nafn',
            'country': 'Land',
            'street_name': 'Heimilisfang',
            'house_number': 'Húsnúmer',
            'city': 'Borg',
            'zip': 'Pósthólf'
        }

    def save(self, commit=True, user=None):
        contact = super().save(commit=False)
        if user:
            contact.user = user
        if commit:
            contact.save()
        return contact

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Staðfesta lykilorð')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        super().clean()
        if not self.user.check_password(self.cleaned_data['old_password']):
            raise forms.ValidationError('Gamla lykilorðið stemmir ekki')
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError('Lykilorðin stemma ekki')
        self.cleaned_data.pop('password_confirm')
        self.cleaned_data.pop('old_password')
        password_validation.validate_password(self.cleaned_data['password'])