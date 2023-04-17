from django.db import models
from django.conf import settings
# Create your models here.

class UserProfile(models.Model):
    profile_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="profile_user",
                                     on_delete=models.CASCADE)
    first_name = models.CharField(max_length=244, default=' ')
    last_name = models.CharField(max_length=244, default=' ')
    phone = models.CharField(max_length=25, default=' ')
    city = models.CharField(max_length=45, default=' ')
    email = models.EmailField(max_length=244)
    profile_image = models.ImageField(upload_to='media/uploads/profile',
                                      blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'