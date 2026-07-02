from django.contrib import admin
from .models import Car, HighlightCar


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'has_discount', 'is_active', 'created_at')
    list_filter = ('has_discount', 'is_active')
    search_fields = ('name',)
    list_editable = ('has_discount', 'is_active')


@admin.register(HighlightCar)
class HighlightCarAdmin(admin.ModelAdmin):
    list_display = ('tab_title', 'car', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
