from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Item, Order, OrderItem

admin.site.unregister(Group)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'get_total_price')
    inlines = (OrderItemInline,)
    readonly_fields = ('created_at',)

    @admin.display(description='Итоговая сумма')
    def total_price(self, obj):
        return obj.get_total_price


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'count')
