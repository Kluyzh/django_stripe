from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Item

admin.site.unregister(Group)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name',)
