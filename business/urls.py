from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import register_business, dashboard

urlpatterns = [
    path('register/', register_business, name='register_business'),
    path('dashboard/', dashboard, name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)