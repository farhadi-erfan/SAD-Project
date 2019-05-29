from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Contributor, User, Requester


class ContributorAdmin(UserAdmin):
    list_display = ['name']
    model = User


admin.site.register(User, ContributorAdmin)
admin.site.register(Contributor)
admin.site.register(Requester)