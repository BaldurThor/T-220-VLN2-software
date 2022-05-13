from django.contrib import admin

from user import models

admin.site.register(models.UserProfile)
admin.site.register(models.Contact)
admin.site.register(models.Rating)
