from django.urls import path
from .views import landing, about, contact, services

urlpatterns = [
    path('', landing, name='landing'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('services/', services, name='service'),
]