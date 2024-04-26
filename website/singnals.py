from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ride
from django.utils import timezone

@receiver(post_save, sender=Ride)
def delete_expired_rides(sender, instance, **kwargs):
    if instance.ride_status == 'scheduled' and instance.start_time < timezone.now():
        instance.delete()
