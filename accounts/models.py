from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    id_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(r'^[0-9]+$', 'Only digits allowed.')],
        help_text="Kenyan National ID or Passport Number",
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        help_text="Format: +254700000000",
        null=True,
        blank=True
    )
    physical_address = models.TextField(blank=True)
    
    # Required fields for Django's auth system
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    # Role methods
    def get_role(self):
        if self.is_superuser:
            return "admin"
        elif self.is_staff:
            return "staff"
        else:
            return "user"

    def is_admin(self):
        return self.is_superuser

    def is_staff_member(self):
        return self.is_staff

    def is_regular_user(self):
        return not self.is_staff and not self.is_superuser