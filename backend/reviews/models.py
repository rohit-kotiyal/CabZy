from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from rides.models import Ride



class Review(models.Model):
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE, related_name='review')
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review for Ride #{self.ride.id} - {self.rating}*"
