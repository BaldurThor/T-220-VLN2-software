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


class RegistrationForm(forms.Form):
    username = forms.CharField(validators=[validate_username])
    email = forms.EmailField()
    fullname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError('Lykilorðin stemma ekki')
        self.cleaned_data.pop('password_confirm')
        password_validation.validate_password(self.cleaned_data['password'])

        fullname = self.cleaned_data['fullname'].strip()
        self.cleaned_data.pop('fullname')
        i = fullname.rfind(' ')
        if i:
            self.cleaned_data['last_name'] = fullname[i:]
            self.cleaned_data['first_name'] = fullname[:i].strip()
        else:
            self.cleaned_data['last_name'] = ''
            self.cleaned_data['first_name'] = fullname

class MyClearableFileInput(ClearableFileInput):
    initial_text = 'núverandi'
    input_text = 'Breyta'
    clear_checkbox_label = 'Eyða mynd'


class UpdateProfileForm(forms.ModelForm):
    image = forms.ImageField(label='Mynd', required=False, widget=MyClearableFileInput)
    banner = forms.ImageField(label='Forsíðu mynd', required=False, widget=MyClearableFileInput)

    class Meta:
        model = models.UserProfile
        fields = ['bio', 'image', 'banner']

    def clean_imagefield(self, field_name):
        image = self.cleaned_data.get(field_name, False)
        if image:
            if image.size > 10*1024*1024:
                raise forms.ValidationError('Mynd of stór! (> 10mb )')
            return image
        else:
            raise forms.ValidationError('Gat ekki lesið file')

    def clean_image(self):
        return self.clean_imagefield('image')

    def clean_banner(self):
        return self.clean_imagefield('banner')



class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = ['full_name', 'country', 'street_name', 'house_number', 'city', 'zip']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

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