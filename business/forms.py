from django import forms
from .models import Business

class BusinessRegistrationForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'name',
            'business_type',
            'kra_pin',
            'county',
            'physical_address',
            'date_established',
            'id_front',
            'id_back',
            'registration_certificate'
        ]
        widgets = {
            'date_established': forms.DateInput(attrs={'type': 'date'}),
            'business_type': forms.Select(attrs={'class': 'form-control'}),
            'county': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'id_front': 'Front of National ID/Passport',
            'id_back': 'Back of National ID/Passport'
        }