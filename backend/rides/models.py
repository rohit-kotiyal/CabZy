from django.db import models
from users.models import User, DriverProfile


class Ride(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        ASSIGNED    = 'ASSIGNED',    'Assigned'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED   = 'COMPLETED',   'Completed'
        CANCELLED   = 'CANCELLED',   'Cancelled'

    class CancelledBy(models.TextChoices):
        RIDER  = 'RIDER',  'Rider'
        DRIVER = 'DRIVER', 'Driver'
        SYSTEM = 'SYSTEM', 'System'


    id = models.BigAutoField(primary_key=True) 
    rider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rider_rides')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='driver_rides')
    status      = models.CharField(max_length=15, choices=Status.choices, default=Status.REQUESTED)


    # Location
    pickup_lat  = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_lng  = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_address = models.CharField(max_length=255, blank=True)
    drop_lat    = models.DecimalField(max_digits=9, decimal_places=6)
    drop_lng    = models.DecimalField(max_digits=9, decimal_places=6)
    drop_address = models.CharField(max_length=255, blank=True)

     # fare
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fare        = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # cancellation
    cancelled_by  = models.CharField(max_length=10, choices=CancelledBy.choices, blank=True)
    cancel_reason = models.TextField(blank=True)

    # timestamps
    created_at    = models.DateTimeField(auto_now_add=True)
    started_at    = models.DateTimeField(null=True, blank=True)
    completed_at  = models.DateTimeField(null=True, blank=True)


    def __str__(self) -> str:
        return f"Ride #{self.id} - {self.status} ({self.rider})"
    



