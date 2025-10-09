from django.contrib import admin
from .models import LostItem, FoundItem, Item, Notification


admin.site.register(LostItem)
admin.site.register(FoundItem)
admin.site.register(Item)
admin.site.register(Notification)
