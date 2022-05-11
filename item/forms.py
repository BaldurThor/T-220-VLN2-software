from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django import forms
from django.utils.timezone import now

from item.models import Item, Category, Offer, ItemImage


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


class ItemImageUploadForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image', 'alt', ]
        labels = {
            'alt': 'Lýsing á mynd',
            'image': 'Mynd'
        }


class CheckoutContactForm(forms.Form):
    contact = forms.ModelChoiceField(queryset=None, label='Heimilisfang', required=False)

    def __init__(self, *args, **kwargs):
        contact_queryset = kwargs.pop('contact_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['contact'].queryset = contact_queryset


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
