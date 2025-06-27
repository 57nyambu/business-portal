from django.shortcuts import render

def landing(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return render(request, 'management/admin_dashboard.html')
    return render(request, 'core/landing.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def services(request):
    return render(request, 'core/services.html')

def pricing(request):
    return render(request, 'core/pricing.html')