from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.forms import ModelForm
from django import forms
from django.utils.timezone import now

from item.models import Item, Offer, ItemImage


class ItemCreateForm(ModelForm):
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Item
        exclude = ['id']
        fields = ['name', 'description', 'condition', 'image', 'banner', 'country', 'zip', 'categories']
        labels = {
            'name': 'Nafn',
            'description': 'Vörulýsing',
            'condition': 'Ástand',
            'country': 'Land',
            'zip': 'Póstnúmer',
            'categories': 'Vöruflokkar'
        }

    def __init__(self, *args, **kwargs):
        categories_choices = kwargs.pop('categories_choices', None)
        super().__init__(*args, **kwargs)
        if categories_choices:
            self.fields['categories'].choices = categories_choices

    def save(self, commit=True, user=None, categories=None):
        item = super().save(commit=False)
        if user:
            item.seller = user
        if commit:
            item.save()
            if categories:
                item.categories.add(*categories)

class ItemImageUploadForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image', ]
        labels = {
            'image': 'Mynd'
        }


class CheckoutContactForm(forms.Form):
    contact = forms.ModelChoiceField(queryset=None, label='Heimilisfang', required=False)

    def __init__(self, *args, **kwargs):
        contact_queryset = kwargs.pop('contact_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['contact'].queryset = contact_queryset

    def save(self, contact_form=None, checkout_session=None, user=None):
        if not checkout_session:
            checkout_session = {}
        if not self.cleaned_data['contact']:
            if contact_form and contact_form.is_valid():
                contact = contact_form.save(user=user)
                checkout_session['contact_id'] = contact.id
        else:
            checkout_session['contact_id'] = self.cleaned_data['contact'].id
        return checkout_session


class CheckoutPaymentForm(forms.Form):
    card_number = forms.CharField(min_length=16)
    card_name = forms.CharField()
    card_valid_month = forms.IntegerField(min_value=1, max_value=12)
    card_valid_year = forms.IntegerField(min_value=now().year)
    card_cvv = forms.IntegerField()

    def clean_card_number(self):
        card_number = ''.join(filter(str.isdigit, self.cleaned_data['card_number']))
        if len(card_number) != 16:
            raise ValidationError('Kortanúmer skal vera 16 stafir.')
        return card_number


class CheckoutRateForm(forms.Form):
    rating = forms.IntegerField(min_value=0, max_value=10)


class SubmitOfferForm(forms.ModelForm):
    amount = forms.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = Offer
        fields = ['item', 'amount']
