from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import User as AppUser

AuthUser = get_user_model()


# Creates a user in the app model when a user from the authentication system is created
@receiver(post_save, sender=AuthUser)
def create_app_user(sender, instance, created, **kwargs):
    
    if created:

        AppUser.objects.create(
            username=instance.username,
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name,
        )
