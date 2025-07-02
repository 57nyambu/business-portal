from django.shortcuts import render
from business.models import Business
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db.models import Count
from management.views import admin_dashboard

User = get_user_model()

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

def landing(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        admin_dashboard(request)
    return render(request, 'core/landing.html')


def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def services(request):
    return render(request, 'core/services.html')

def pricing(request):
    return render(request, 'core/pricing.html')