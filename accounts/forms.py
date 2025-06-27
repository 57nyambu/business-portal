from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import User

from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-700 text-white placeholder-gray-400 w-full px-4 py-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
            'placeholder': 'John'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-700 text-white placeholder-gray-400 w-full px-4 py-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
            'placeholder': 'Doe'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'bg-gray-700 text-white placeholder-gray-400 w-full px-4 py-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
            'placeholder': 'name@company.com'
        })
    )
    id_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-700 text-white placeholder-gray-400 w-full px-4 py-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
            'placeholder': 'Enter your ID number'
        })
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-700 text-white placeholder-gray-400 w-full px-4 py-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
            'placeholder': '+254700000000'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-700 text-white placeholder-gray-400 w-full px-4 py-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
            'placeholder': 'Enter your password'
        }),
        help_text=None  # Remove help text
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-700 text-white placeholder-gray-400 w-full px-4 py-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
            'placeholder': 'Confirm your password'
        }),
        help_text=None  # Remove help text
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'id_number', 
                 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep the password validation but customize the help text
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        # Make sure email is used as username if your User model uses email as username
        if hasattr(self.Meta.model, 'USERNAME_FIELD') and self.Meta.model.USERNAME_FIELD == 'email':
            self.fields['email'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # If your User model uses email as username, set it here
        if hasattr(user, 'USERNAME_FIELD') and user.USERNAME_FIELD == 'email':
            user.username = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'bg-gray-700 text-white placeholder-gray-400 w-full px-4 py-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
            'placeholder': 'youremail@example.com'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-700 text-white placeholder-gray-400 w-full px-4 py-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
            'placeholder': '••••••••'
        })
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Invalid email or password.',
                    code='invalid_login'
                )
        return self.cleaned_data