from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import register_business, dashboard, business_detail, download_certificate

urlpatterns = [
    path('register/', register_business, name='register_business'),
    path('dashboard/', dashboard, name='dashboard'),
    path('my-businesses/<int:business_id>/', business_detail, name='business_detail'),
    path('my-businesses/<int:business_id>/download/', download_certificate, name='download_certificate')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
