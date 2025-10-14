from django.db import models
from django.contrib.auth.models import User

# -------------------------
# Lost and Found Models
# -------------------------
class LostItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_lost = models.DateField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    found = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class FoundItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_found = models.DateField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='found_items/', blank=True, null=True)

    def __str__(self):
        return self.title


# -------------------------
# General Item Model
# -------------------------
class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date_lost = models.DateField()
    description = models.TextField()
    contact_info = models.CharField(max_length=100)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    is_reported = models.BooleanField(default=False)  # Optional: mark if reported

    def __str__(self):
        return self.name


# -------------------------
# Notification Model
# -------------------------
class Notification(models.Model):
    recipient = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    recipient_contact = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField()
    lost_item = models.ForeignKey(LostItem, null=True, blank=True, on_delete=models.CASCADE)
    found_item = models.ForeignKey(FoundItem, null=True, blank=True, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = self.recipient.username if self.recipient else (self.recipient_contact or "Unknown")
        return f"Notification to {who}: {self.message[:40]}"


# -------------------------
# User Reported Items (Optional)
# -------------------------

class ReportItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date_lost = models.DateField()
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} reported by {self.user.username}"


# -------------------------
# Admin / User Report System
# -------------------------
class Report(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_REVIEWED = 'reviewed'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_REVIEWED, 'Reviewed'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest report first

    def __str__(self):
        reporter_name = self.reporter.username if self.reporter else "Anonymous"
        return f"Report #{self.id} on {self.item.name} by {reporter_name} ({self.status})"


class Notification(models.Model):
    # ধরো user id=1 assign করছ পুরনো rows-এর জন্য
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', default=1)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"