from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse, NoReverseMatch
from django.utils.timezone import now

from item.forms import CheckoutContactForm, CheckoutPaymentForm, CheckoutRateForm
from item.models import Offer, Sale
from user.forms import ContactForm
from user.models import Contact, Country, Rating

CHECKOUT_STEPS = {
    'item:checkout_contact': 'Heimilisfang',
    'item:checkout_payment': 'Greiðsluvalmöguleikar',
    'item:checkout_rate': 'Seljanda einkunn',
    'item:checkout_verify': 'Staðfesting',
}


def __get_steps(request):
    print(request.session.get('checkout'))
    steps = []
    for step_url, step_name in CHECKOUT_STEPS.items():
        step = {
            'url': step_url,
            'path': reverse(step_url),
            'name': step_name,
            'active': False,
            'available': True
        }
        if request.path == step['path']:
            step['active'] = True
        if step['url'] == 'item:checkout_verify':
            checkout_session = request.session.get('checkout', False)
            if not checkout_session:
                step['available'] = False
            elif (
                not checkout_session.get('offer_id')
                or not checkout_session.get('contact_id')
                or not checkout_session.get('payment_information')
            ):
                step['available'] = False
        steps.append(step)
    return steps


def __get_summary(request):
    summary = {}
    checkout_session = request.session.get('checkout', [])
    try:
        summary['contact'] = Contact.objects.get(pk=checkout_session.get('contact_id'))
    except Contact.DoesNotExist:
        pass
    if payment_information := checkout_session.get('payment_information'):
        summary['payment_information'] = payment_information
    try:
        summary['rating'] = Rating.objects.get(pk=checkout_session.get('rating_id'))
    except Rating.DoesNotExist:
        pass
    return summary


def checkout(request, offer_id):
    offer = Offer.objects.get(pk=offer_id, accepted=True, user=request.user)
    request.session['checkout'] = {
        'offer_id': offer.id
    }
    return redirect('item:checkout_contact')


def checkout_contact(request):
    checkout_session = request.session.get('checkout', False)
    if not checkout_session:
        return redirect('item:get_all_offers')
    offer = Offer.objects.get(pk=checkout_session['offer_id'], accepted=True, user=request.user)
    contacts = Contact.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CheckoutContactForm(request.POST, contact_queryset=contacts)
        if form.is_valid():
            if not form.cleaned_data['contact']:
                contact_form = ContactForm(request.POST)
                if contact_form.is_valid():
                    contact = contact_form.save(commit=False)
                    contact.user = request.user
                    contact.save()
                    checkout_session['contact_id'] = contact.id
            else:
                checkout_session['contact_id'] = form.cleaned_data['contact'].id
            request.session['checkout'] = checkout_session
            return redirect('item:checkout_payment')
    else:
        contact_id = checkout_session.get('contact_id')
        data = {}
        if contact_id:
            data['contact'] = Contact.objects.get(pk=contact_id)
        form = CheckoutContactForm(data, contact_queryset=contacts)

        contact = Contact(full_name=request.user.get_full_name())
        try:
            contact.country = Country.objects.get(name='Iceland')
        except Country.DoesNotExist:
            pass
        contact_form = ContactForm(instance=contact)

    context = {
        'offer': offer,
        'form': form,
        'contact_form': contact_form,
        'summary': __get_summary(request),
        'checkout_steps': __get_steps(request),
    }
    return render(request, 'item/checkout/contact.html', context)


def checkout_payment(request):
    checkout_session = request.session.get('checkout', False)
    if not checkout_session:
        return redirect('item:get_all_offers')
    offer = Offer.objects.get(pk=checkout_session['offer_id'], accepted=True, user=request.user)
    if request.method == 'POST':
        form = CheckoutPaymentForm(request.POST)
        if form.is_valid():
            checkout_session['payment_information'] = form.cleaned_data
            request.session['checkout'] = checkout_session
            return redirect('item:checkout_rate')
    else:
        data = None
        if payment_information := checkout_session.get('payment_information'):
            print(payment_information)
            data = payment_information
        form = CheckoutPaymentForm(data)
    context = {
        'offer': offer,
        'form': form,
        'summary': __get_summary(request),
        'checkout_steps': __get_steps(request),
    }
    return render(request, 'item/checkout/payment.html', context)


def checkout_rate(request):
    checkout_session = request.session.get('checkout', False)
    if not checkout_session:
        return redirect('item:get_all_offers')
    offer = Offer.objects.get(pk=checkout_session['offer_id'], accepted=True, user=request.user)
    if request.method == 'POST':
        form = CheckoutRateForm(request.POST)
        if form.is_valid():
            checkout_session['rate_information'] = form.cleaned_data
            try:
                rating = Rating.objects.get(rater=request.user, rated=offer.item.seller)
            except Rating.DoesNotExist:
                rating = Rating(rater=request.user, rated=offer.item.seller)
            rating.rating = form.cleaned_data['rating']
            rating.save()
            checkout_session['rating_id'] = rating.id
            request.session['checkout'] = checkout_session
            return redirect('item:checkout_verify')
    else:
        form = CheckoutRateForm()

    context = {
        'offer': offer,
        'form': form,
        'summary': __get_summary(request),
        'checkout_steps': __get_steps(request)
    }
    return render(request, 'item/checkout/rate.html', context)


def checkout_verify(request):
    checkout_session = request.session.get('checkout', False)
    submittable = True
    if not checkout_session:
        return redirect('item:get_all_offers')
    offer = Offer.objects.get(pk=checkout_session.get('offer_id'), accepted=True, user=request.user)
    try:
        contact = Contact.objects.get(pk=checkout_session.get('contact_id'))
    except Contact.DoesNotExist:
        contact = None
        submittable = False

    payment_information = checkout_session.get('payment_information')
    if not payment_information:
        submittable = False
    if request.method == 'POST' and submittable:
        sale = Sale()
        sale.fill_from_contact(contact)
        sale.fill_from_offer(offer)
        for field, value in payment_information.items():
            setattr(sale, field, value)
        sale.sold_at = now()
        sale.save()
        request.session.pop('checkout')
        request.session['checkout_thanks'] = True
        return redirect('item:checkout_thanks')
    context = {
        'offer': offer,
        'checkout_steps': __get_steps(request),
        'summary': __get_summary(request),
        'contact': contact,
        'payment_information': checkout_session.get('payment_information'),
        'submittable': submittable,
    }
    return render(request, 'item/checkout/verify.html', context)


def checkout_thanks(request):
    if not request.session.get('checkout_thanks', False):
        return redirect('item:get_all_offers')
    request.session.pop('checkout_thanks')
    return render(request, 'item/checkout/thanks.html')
