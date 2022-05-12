from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from item import services
from item.forms import ItemCreateForm, ItemImageUploadForm
from item.models import Category, Item, ItemImage, Offer
from user.models import Country, UserProfile


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
            if item_image_ids := request.session.get('item_images', []):
                print(item_image_ids)
                item_images = ItemImage.objects.filter(pk__in=item_image_ids)
                for item_image in item_images:
                    item_image.item = item
                    item_image.save()
                request.session['item_images'] = []
            if images := request.FILES.getlist('images'):
                for image in images:
                    item_image = ItemImage(item=item, image=image)
                    item_image.save()

            messages.add_message(request, messages.SUCCESS, 'Varan hefur verið stofnuð.')
            return redirect('item:catalog')
    else:
        request.session['item_images'] = []
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
def upload_item_image(request, item_id=None):
    if request.method == 'POST':
        form = ItemImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            item_image = form.save()
            if not item_id:
                item_images_session = request.session.get('item_images', [])
                item_images_session.append(item_image.id)
                request.session['item_images'] = item_images_session
        else:
            return JsonResponse(form.errors)
    return JsonResponse({})


def get_item(request, id):
    item = get_object_or_404(Item, pk=id)
    view_session = request.session.get('viewed_items', [])
    if item.id not in view_session:
        item.views += 1
        item.save()
        view_session.append(item.id)
        request.session['viewed_items'] = view_session
    seller = UserProfile.objects.get(user=item.seller)
    context = {'item': item, 'seller': seller}
    similar_items = services.get_similar(item)
    if similar_items:
        context['similar_items'] = similar_items
    try:
        offer = Offer.objects.order_by('-amount').filter(item=item, rejected=False)[0]
        context['offer'] = offer
    except Offer.DoesNotExist:
        pass
    except IndexError:
        pass
    return render(request, 'item/get_item.html', context)
