from django.contrib import admin
from item import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Condition)
admin.site.register(models.Item)
admin.site.register(models.ItemImage)
admin.site.register(models.Offer)
admin.site.register(models.Sale)
