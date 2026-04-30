from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db) 
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        RIDER  = 'RIDER',  'Rider'
        DRIVER = 'DRIVER', 'Driver'
        ADMIN  = 'ADMIN',  'Admin'

    username = None
    email    = models.EmailField(unique=True)
    phone    = models.CharField(max_length=10, blank=True)
    role     = models.CharField(max_length=10, choices=Role.choices)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []          

    objects = UserManager()        #type: ignore

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_rider(self):
        return self.role == self.Role.RIDER

    @property
    def is_driver(self):
        return self.role == self.Role.DRIVER

    @property
    def is_cab_admin(self):
        return self.role == self.Role.ADMIN
    


class RiderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_profile')
    default_pickup = models.CharField(max_length=255, blank=True)


    def __str__(self) -> str:
        return f"Rider: {self.user.email}"
    

class DriverProfile(models.Model):
    class VehicleType(models.TextChoices):
        BIKE = 'BIKE', 'Bike'
        AUTO = 'AUTO', 'Auto'
        CAR  = 'CAR',  'Car'
        SUV  = 'SUV',  'SUV'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    vehicle_type = models.CharField(max_length=10, choices=VehicleType.choices)
    vehicle_no   = models.CharField(max_length=20)
    license_no   = models.CharField(max_length=20)
    is_approved  = models.BooleanField(default=False)  # admin verifies this
    is_available = models.BooleanField(default=False)  # driver toggles online/offline
    current_lat  = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_lng  = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)


    def __str__(self) -> str:
        return f"Driver: {self.user.email} ({self.vehicle_type})"
    

