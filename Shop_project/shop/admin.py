from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    list_display = ('id', 'name', 'price', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'price')
    list_filter = ('name', 'price')
    fields = ('name', 'description', 'price')
    readonly_fields = ('id',)
    ordering = ['name', 'price']
    save_on_top = True


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('number', 'items_list', 'discount_types', 'total_discount', 'total_tax', 'total_price')
    list_display_links = ('number',)
    search_fields = ('number',)
    ordering = ['number']
    save_on_top = True

    def items_list(self, obj):
        return ", ".join([f"id: {item.item.pk} (q: {item.quantity})" for item in obj.orderitem_set.all()])

    def total_tax(self, obj):
        return obj.total_tax()

    def total_discount(self, obj):
        return obj.total_discount()

    def discount_types(self, obj):
        return ", ".join([discount.name for discount in obj.discounts.all()])

    items_list.short_description = 'Items'  # Название для колонки в списке
    total_tax.short_description = 'Total Tax'
    total_discount.short_description = 'Total Discount'
    discount_types.short_description = 'Discount Types'


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ('order', 'item', 'quantity')
    ordering = ['order', 'quantity', 'item']


@admin.register(Discount)
class DiscountAdmin(ModelAdmin):
    list_display = ('name', 'percentage')
    list_display_links = ('name', 'percentage')
    fields = ('name', 'percentage')
    ordering = ['percentage', 'name']


@admin.register(Tax)
class TaxAdmin(ModelAdmin):
    list_display = ('name', 'percentage')
    list_display_links = ('name', 'percentage')
    fields = ('name', 'percentage')
    ordering = ['percentage', 'name']
