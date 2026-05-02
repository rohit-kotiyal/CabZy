from django.db import models
from rides.models import Ride


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = 'CASH', 'Cash'
        ONLINE = 'ONLINE', 'Online'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'


    ride = models.OneToOneField(Ride, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=10, choices=Method.choices, default=Method.CASH)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    gateway_ref = models.CharField(max_length=100, blank=True)  #Razorpay/Stripe payment ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Payment #{self.id} - Ride #{self.ride.id} - {self.status}"
    


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_pct = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100
    max_uses = models.IntegerField(default=1)
    used_count = models.IntegerField(default=0)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.code} ({self.discount_pct}% off)"
    

    def is_valid(self):
        from django.utils import timezone
        return (
            self.is_active and
            self.used_count < self.max_uses and
            self.expires_at > timezone.utc()
        )


