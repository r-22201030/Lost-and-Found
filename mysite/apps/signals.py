from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import FoundItem, LostItem, Notification,ReportItem

@receiver(post_save, sender=FoundItem)
def notify_on_found_item(sender, instance, created, **kwargs):

    if not created:
        return

    found = instance

    # 1) exact matches first
    matches = LostItem.objects.filter(title__iexact=found.title, location__iexact=found.location)

    # 2)  partial match
    if not matches.exists():
        matches = LostItem.objects.filter(title__icontains=found.title) | LostItem.objects.filter(location__icontains=found.location)

    # distinct to avoid duplicates
    matches = matches.distinct()

    for lost in matches:
        message = (
            f"Possible match: Your lost item '{lost.title}' may have been found.\n"
            f"Found at: {found.location} on {found.date_found}. "
            f"Found description: {found.description[:200]}"
        )

        # prefer user if reported_by set, else use contact_info from lost
        recipient_user = getattr(lost, 'reported_by', None)
        recipient_contact = getattr(lost, 'contact_info', None)

        notif = Notification.objects.create(
            recipient=recipient_user if recipient_user else None,
            recipient_contact=recipient_contact if not recipient_user else '',
            message=message,
            lost_item=lost,
            found_item=found,
        )

        # optional: send an email if user has email and EMAIL is configured
        try:
            if recipient_user and recipient_user.email:
                send_mail(
                    subject="Lost item might be found",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient_user.email],
                    fail_silently=True,
                )
        except Exception as e:
            # dev-time: you can log this. We keep silent so production doesn't crash.
            pass


@receiver(post_save, sender=FoundItem)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # ধরা যাক FoundItem-এর title-এর সাথে matching report খুঁজছ
        reports = ReportItem.objects.filter(item_name__iexact=instance.title)
        for report in reports:
            Notification.objects.create(
                user=report.user,
                message=f"Your reported item '{report.item_name}' has been found!",
                link=f"/found_item/{instance.id}/"
            )