from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from pytz import utc

from .tasks import process_active_distribution


@receiver(post_save, sender="api.Distribution")
def on_post_save_distribution(sender, instance, created, **kwargs):
    if created and instance.amount < datetime.now(utc):
        process_active_distribution.apply_async(args=[instance.id])
