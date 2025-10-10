from django.contrib import admin
from .models import LostItem, FoundItem, Item, Notification, ReportItem


@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date_lost')
    search_fields = ('title', 'location', 'description')
    list_filter = ('date_lost',)


@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date_found')
    search_fields = ('title', 'location', 'description')
    list_filter = ('date_found',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'date_lost')
    search_fields = ('name', 'category', 'location', 'description')
    list_filter = ('category', 'date_lost')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(ReportItem)
class ReportItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'user', 'location', 'date_lost', 'created_at')
    search_fields = ('item_name', 'user__username', 'location', 'description')
    list_filter = ('date_lost', 'created_at')
    readonly_fields = ('created_at',)
