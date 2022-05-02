from django.forms import ModelForm, widgets
from django import forms
from item.models import Item, Condition
from user.models import Country


class ItemCreateForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['id']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item name'}),
            'description': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'condition': widgets.Select(attrs={'class': 'form-control'}),
            'country': widgets.Select(attrs={'class': 'form-control'}),
            #'price': widgets.NumberInput(attrs={'class': 'form-control'}),
            #'manufacturer': widgets.Select(attrs={'class': 'form-control'}),
            #'on_sale': widgets.CheckboxInput(attrs={'class': 'checkbox'}),
        }



"""
class ItemCreateForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    image_url = forms.URLField()
    zip = forms.CharField()
    sold_at = forms.DateField()
    condition = forms.ChoiceField(Condition.objects.all())
    country = forms.ChoiceField(Country.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
"""