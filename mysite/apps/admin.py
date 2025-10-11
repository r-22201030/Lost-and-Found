# apps/admin.py
from django.contrib import admin
from .models import LostItem, FoundItem, Item, Notification, ReportItem, Report


# -------------------------
# Lost Item Admin
# -------------------------
@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date_lost')
    search_fields = ('title', 'location', 'description')
    list_filter = ('date_lost',)


# -------------------------
# Found Item Admin
# -------------------------
@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date_found')
    search_fields = ('title', 'location', 'description')
    list_filter = ('date_found',)


# -------------------------
# Inline Report (Item এর নিচে রিপোর্ট দেখা)
# -------------------------
class ReportInline(admin.TabularInline):
    model = Report
    extra = 0
    readonly_fields = ('reporter', 'reason', 'description', 'status', 'created_at')
    can_delete = False


# -------------------------
# Item Admin (report সহ)
# -------------------------
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'date_lost', 'is_reported', 'reported_count')
    search_fields = ('name', 'category', 'location', 'description')
    list_filter = ('category', 'date_lost', 'is_reported')
    inlines = [ReportInline]

    def reported_count(self, obj):
        return obj.reports.count()
    reported_count.short_description = 'Report Count'


# -------------------------
# Notification Admin
# -------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('created_at',)


# -------------------------
# ReportItem (User Reported Item)
# -------------------------
@admin.register(ReportItem)
class ReportItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'user', 'location', 'date_lost', 'created_at')
    search_fields = ('item_name', 'user__username', 'location', 'description')
    list_filter = ('date_lost', 'created_at')
    readonly_fields = ('created_at',)


# -------------------------
# Admin-side Report Table (auto visible report)
# -------------------------
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'reporter', 'reason', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('item__name', 'reporter__username', 'reason', 'description')
    readonly_fields = ('item', 'reporter', 'reason', 'description', 'created_at')
    actions = ['mark_reviewed']

    def mark_reviewed(self, request, queryset):
        """
        ✅ নির্বাচিত রিপোর্টগুলো 'reviewed' করে দিবে
        এবং Item.is_reported False করে দেবে (যদি pending না থাকে)
        """
        updated = 0
        for report in queryset:
            report.status = Report.STATUS_REVIEWED
            report.save(update_fields=['status'])
            # যদি আর pending report না থাকে তাহলে item এর ফ্ল্যাগ false করো
            item = report.item
            if not item.reports.filter(status=Report.STATUS_PENDING).exists():
                item.is_reported = False
                item.save(update_fields=['is_reported'])
                updated += 1
        self.message_user(request, f"{updated} item(s) marked as reviewed.")
    mark_reviewed.short_description = "Mark selected reports as reviewed"
