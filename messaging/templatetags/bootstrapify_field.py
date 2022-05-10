from django import template
from django.forms import CheckboxSelectMultiple

register = template.Library()


@register.filter(name='bootstrapify_field')
def bootstrapify_form_element(field):
    attrs = field.subwidgets[0].data['attrs']
    if not (field.field.widget and hasattr(field.field.widget, 'input_type') and field.field.widget.input_type == 'checkbox'):
        if 'class' not in attrs:
            attrs['class'] = 'form-control'
        else:
            attrs['class'] += ' form-control'
    if len(field.errors) > 0:
        attrs['class'] += ' is-invalid'
    return field.as_widget(attrs=attrs)
