from pprint import pprint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from item.models import Item
from user.forms import RegistrationForm, UpdateProfileForm, ContactForm, ChangePasswordForm
from user.models import UserProfile, Contact, Country
# Create your views here.


def frontpage(request):
    most_viewed_items = Item.objects.order_by('-views').filter(is_deleted=False, accepted_offer=None)[0:4]
    context = {
        'items': Item.objects.order_by('?').filter(is_deleted=False, accepted_offer=None)[0:3],
        'most_viewed_items': most_viewed_items,
    }
    return render(request, 'user/frontpage.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(**form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_profile = UserProfile(user=user)
            user_profile.save()
            return redirect('user:login')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'user/register.html', context)


@login_required
def profile(request, user_id=None):
    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = request.user
    context = {
        'user_profile': UserProfile.objects.get(user=user)
    }
    return render(request, 'user/profile.html', context)


@login_required
def update_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
    else:
        form = UpdateProfileForm(instance=user_profile)
    context = {
        'form': form
    }
    return render(request, 'user/update_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('user:profile')
    else:
        form = ChangePasswordForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'user/change_password.html', context)


@login_required
def get_all_contacts(request):
    contacts = Contact.objects.filter(user=request.user)
    context = {
        'contacts': contacts
    }
    return render(request, 'user/get_all_contacts.html', context)


@login_required
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        return redirect('user:get_all_contacts')
    else:
        contact = Contact(full_name=request.user.get_full_name())
        try:
            contact.country = Country.objects.get(name='Iceland')
        except Country.DoesNotExist:
            pass
        form = ContactForm(instance=contact)
    context = {
        'form': form,
    }
    return render(request, 'user/create_contact.html', context)


@login_required
def update_contact(request, contact_id):
    contact = Contact.objects.get(pk=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        form.save()
        return redirect('user:get_all_contacts')
    else:
        form = ContactForm(instance=contact)
    context = {
        'form': form,
    }
    return render(request, 'user/create_contact.html', context)
