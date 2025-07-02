from django.urls import path

from .views import admin_dashboard, update_business_status
urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('update-business-status/<int:business_id>/', update_business_status, name='update_business_status'),
]