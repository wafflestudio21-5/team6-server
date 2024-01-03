from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import WaffleUser

# Register your models here.
admin.site.register(WaffleUser)
# admin.site.register(UserAdmin)
