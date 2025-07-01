from django.contrib import admin
from .models import Business, PartnershipDetail, CompanyDetail

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'business_type', 'registration_number', 'kra_pin', 'county', 'status', 'created_at')
    search_fields = ('name', 'kra_pin', 'county', 'registration_number')
    list_filter = ('business_type', 'status', 'county')
    readonly_fields = ('created_at', 'registration_number', 'registration_certificate')  # registration_number is read-only

@admin.register(PartnershipDetail)
class PartnershipDetailAdmin(admin.ModelAdmin):
    list_display = ('business', 'partners_name', 'partners_id_numbers')
    search_fields = ('partners_name', 'partners_id_numbers')

@admin.register(CompanyDetail)
class CompanyDetailAdmin(admin.ModelAdmin):
    list_display = ('business', 'directors', 'share_capital')
    search_fields = ('directors',)
