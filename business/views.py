from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import BusinessRegistrationForm

@login_required
def register_business(request):
    if request.method == 'POST':
        form = BusinessRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            return redirect('dashboard')
    else:
        form = BusinessRegistrationForm()
    return render(request, 'business/registration.html', {'form': form})

@login_required
def dashboard(request):
    businesses = request.user.business_set.all()
    context = {
        'businesses': businesses,
        'media_url': settings.MEDIA_URL
    }
    return render(request, 'business/dashboard.html', context)