from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Restaurant Owner', 'Restaurant Owner'),
        ('Delivery Personnel', 'Delivery Personnel'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')
