from django.contrib import admin
from .models import *


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'price')
    list_filter = ('name', 'price')
    fields = ('name', 'description', 'price')
    readonly_fields = ('id',)
    save_on_top = True
