from django.db import models
from users.models import User



class Notification(models.Model):
    class Type(models.TextChoices):
        RIDE_REQUESTED  = 'RIDE_REQUESTED',  'Ride Requested'
        RIDE_ASSIGNED   = 'RIDE_ASSIGNED',   'Ride Assigned'
        RIDE_STARTED    = 'RIDE_STARTED',    'Ride Started'
        RIDE_COMPLETED  = 'RIDE_COMPLETED',  'Ride Completed'
        RIDE_CANCELLED  = 'RIDE_CANCELLED',  'Ride Cancelled'
        PAYMENT_DONE    = 'PAYMENT_DONE',    'Payment Done'
        DRIVER_APPROVED = 'DRIVER_APPROVED', 'Driver Approved'


    user = models.ForeignKey(User, on_delete=models.CASCADE, name='notifications')
    type = models.CharField(max_length=20, choices=Type.choices)
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification -> {self.user.email} | {self.type}"
    
    