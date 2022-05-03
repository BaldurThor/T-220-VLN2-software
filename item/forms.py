from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django import forms
from item.models import Item, Category


class ItemCreateForm(ModelForm):

    class Meta:
        model = Item
        exclude = ['id']
        fields = ['name', 'description', 'condition', 'image_url', 'country', 'zip', 'published_at', 'categories']
