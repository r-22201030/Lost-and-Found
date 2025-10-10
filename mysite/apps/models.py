from django.db import models
from django.contrib.auth.models import User

class LostItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_lost = models.DateField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)

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


class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date_lost = models.DateField()
    description = models.TextField()
    contact_info = models.CharField(max_length=100)
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    def __str__(self):
        return self.name


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
