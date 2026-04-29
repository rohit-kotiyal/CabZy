from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # fix: self._db
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