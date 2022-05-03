from pprint import pprint

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from item.models import Item
from user.forms import RegistrationForm


def frontpage(request):
    context = {
        'items': Item.objects.order_by('?')[0:3]
    }
    return render(request, 'user/frontpage.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(**form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('user:login')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'user/register.html', context)
