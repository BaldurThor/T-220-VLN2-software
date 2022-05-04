from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User

from user.models import UserProfile


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


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'image_url']
