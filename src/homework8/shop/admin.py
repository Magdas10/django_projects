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
    list_display = ('id', 'customer', 'items')


class PurchaseAdmin(admin.ModelAdmin):
    ordering = ['items']
    list_display = ('id', 'items', 'buy_time', 'customer')


admin.site.register(StoreCategory, StoreCategoryAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(StoreOwner, StoreOwnerAdmin)
