from django.dispatch import receiver
from django.db.models.signals import post_save
from user_profile.models import UserProfile
from .models import CustomUserModel

user = CustomUserModel


@receiver(post_save, sender=user)
def create_profile(sender, instance, created, **kwargs):
    user = CustomUserModel.objects.last()
    if created:
        UserProfile.objects.create(profile_user=instance, first_name=user.username, last_name='', phone='9999-9999', city='unknown', email=user.email, profile_image=' ')