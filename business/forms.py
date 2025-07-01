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
        labels = {
            'name': 'Business name',
        }

class PartnershipDetailForm(forms.ModelForm):
    class Meta:
        model = PartnershipDetail
        fields = ['partners_name', 'partners_id_numbers']

class CompanyDetailForm(forms.ModelForm):
    class Meta:
        model = CompanyDetail
        fields = ['directors', 'share_capital']