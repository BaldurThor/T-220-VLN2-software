from django.contrib import admin

from user.models import *

admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Rating)
