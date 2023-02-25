from django.contrib import admin
from .models import *


class StoreCategoryAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('id', 'name')


class ItemCategoryAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('id', 'name')


class CustomerAdmin(admin.ModelAdmin):
    ordering = ['-registrated_at']
    list_display = ('id', 'user', 'registrated_at')


class StoreOwnerAdmin(admin.ModelAdmin):
    ordering = ['-registrated_at']
    list_display = ('id', 'user', 'registrated_at')


class StoreAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('id', 'name', 'owner', 'store_category')


class ItemAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('id', 'name', 'category', 'price', 'quantity', 'info', 'store')


class MyBagAdmin(admin.ModelAdmin):
    ordering = ['customer']

    def get_items(self, obj):
        obj.total()
        return ",".join([item.name for item in obj.items.all()])

    list_display = ('id', 'customer', 'get_items', 'total_price')


class PurchaseAdminError(Exception):
    pass


class PurchaseAdmin(admin.ModelAdmin):
    # ordering = ['items']

    def get_items(self, obj):
        obj.quantity()
        return "\n".join([item.name for item in obj.items.all()])

    list_display = ('id', 'get_items', 'buy_time', 'total_price')


admin.site.register(StoreCategory, StoreCategoryAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(StoreOwner, StoreOwnerAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(MyBag, MyBagAdmin)
admin.site.register(Purchase, PurchaseAdmin)
