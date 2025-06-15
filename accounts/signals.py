from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def new_user_registration(sender, instance, created, **kwargs):
    if created:
        # Send verification email
        # Or other post-registration actions
        pass