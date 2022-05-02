from django import template
register = template.Library()


@register.filter(name='bootstrapify_field')
def bootstrapify_form_element(field):
    print(len(field.errors))
    attrs = field.subwidgets[0].data['attrs']
    if 'class' not in attrs:
        attrs['class'] = 'form-control'
    else:
        attrs['class'] += ' form-control'
    if len(field.errors) > 0:
        attrs['class'] += ' is-invalid'
    return field.as_widget(attrs=attrs)
