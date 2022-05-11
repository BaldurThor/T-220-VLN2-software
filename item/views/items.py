from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from item.forms import ItemCreateForm, ItemImageUploadForm
from item.models import Category, Item, ItemImage
from user.models import Country


@login_required
def create_item(request):
    categories_choices = Category.objects.values_list('id', 'name')

    if request.method == 'POST':
        form = ItemCreateForm(request.POST, request.FILES, categories_choices=categories_choices)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            values = request.POST.getlist('categories')
            item.categories.add(*values)

            if images := request.FILES.getlist('images'):
                for image in images:
                    item_image = ItemImage(item=item, image=image)
                    item_image.save()

            messages.add_message(request, messages.SUCCESS, 'Varan hefur verið stofnuð.')
            return redirect('item:catalog')
    else:
        item = Item()
        try:
            item.country = Country.objects.get(name='Iceland')
        except Country.DoesNotExist:
            pass
        form = ItemCreateForm(
            instance=item,
            categories_choices=categories_choices
        )
        image_form = ItemImageUploadForm()
    return render(request, 'item/create_item.html', {
        'form': form,
        'image_form': image_form,
    })

@login_required
def upload_item_image(request):
    pass
