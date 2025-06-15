from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'id_number',
            'phone_number',
            'physical_address',
            'password1',
            'password2'
        ]
        labels = {
            'id_number': 'National ID/Passport No.'
        }