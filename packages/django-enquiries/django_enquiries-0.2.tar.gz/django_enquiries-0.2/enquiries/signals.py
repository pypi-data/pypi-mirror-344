from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import BaseEnquiry

@receiver(post_save, sender=BaseEnquiry)
def set_ticket_number(sender, instance, created, **kwargs):
    if created:
        instance.set_ticket_number()