from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    # Additional fields beyond default User model
    id_number = models.CharField(max_length=20,
        unique=True,
        validators=[RegexValidator(r'^[0-9]+$', 'Only digits allowed.')],
        help_text="Kenyan National ID or Passport Number"
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        help_text="Format: +254700000000"
    )
    physical_address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_full_name()} ({self.id_number})"