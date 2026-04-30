from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RiderProfile, DriverProfile, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return
    
    if instance.role == User.Role.RIDER:
        RiderProfile.objects.create(user=instance)

    if instance.role == User.Role.DRIVER:
        DriverProfile.objects.create(user=instance)
