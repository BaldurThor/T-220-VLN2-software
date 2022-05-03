from .models import Category


def categories(request):
    return {
        'categories': Category.objects.order_by('name').all()
    }
