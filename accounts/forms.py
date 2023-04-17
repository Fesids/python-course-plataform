from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUserModel


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUserModel
        fields = UserCreationForm.Meta.fields + ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUserModel
        fields = UserChangeForm.Meta.fields
