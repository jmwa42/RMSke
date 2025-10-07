# core/signals.py
import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment

@receiver(post_save, sender=Payment)
def notify_whatsapp_bot(sender, instance, created, **kwargs):
    if created and instance.status == "CONFIRMED":
        payload = {
            "tenant": instance.tenant.name,
            "phone": instance.tenant.phone_number,
            "amount": str(instance.amount),
            "invoice_id": instance.invoice.id if instance.invoice else None,
            "date": instance.date.isoformat(),
        }

        bot_url = getattr(settings, "BOT_WEBHOOK_URL", None)
        if not bot_url:
            print("⚠️ BOT_WEBHOOK_URL not set in environment or settings.py")
            return

        try:
            resp = requests.post(bot_url, json=payload, timeout=5)
            resp.raise_for_status()
            print(f"✅ Webhook sent to bot: {resp.status_code}")
        except Exception as e:
            print("⚠️ Webhook error:", e)

