from django import forms
from .models import Business, PartnershipDetail, CompanyDetail

class BusinessRegistrationForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'name', 'business_type', 'kra_pin', 'county',
            'physical_address', 'date_established',
            'id_front', 'id_back'
        ]
        widgets = {
            'date_established': forms.DateInput(attrs={'type': 'date'}),
        }

class PartnershipDetailForm(forms.ModelForm):
    class Meta:
        model = PartnershipDetail
        fields = ['partners']

class CompanyDetailForm(forms.ModelForm):
    class Meta:
        model = CompanyDetail
        fields = ['directors', 'shareholders', 'share_capital']
