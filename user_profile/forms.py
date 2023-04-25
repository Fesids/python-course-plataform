from django import forms
from .models import UserProfile


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profile_image', 'first_name', 'last_name', 'city', 'phone', 'email']