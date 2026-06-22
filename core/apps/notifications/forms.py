from django.contrib.auth.forms import AuthenticationForm


from core.apps.users.models import CustomUser
from django import forms


class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your username"}
        ),
    )
    password = forms.CharField(
        label="Username",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Your password"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["username", "password"]
