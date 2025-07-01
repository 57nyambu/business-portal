from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import BusinessRegistrationForm, PartnershipDetailForm, CompanyDetailForm
from .models import Business

@login_required
def register_business(request):
    if request.method == 'POST':
        form = BusinessRegistrationForm(request.POST, request.FILES)
        business_type = request.POST.get('business_type')

        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()

            # Handle type-specific detail
            if business_type == 'partnership':
                partner_form = PartnershipDetailForm(request.POST)
                if partner_form.is_valid():
                    partner = partner_form.save(commit=False)
                    partner.business = business
                    partner.save()
            elif business_type == 'company':
                company_form = CompanyDetailForm(request.POST)
                if company_form.is_valid():
                    company = company_form.save(commit=False)
                    company.business = business
                    company.save()

            return redirect('dashboard')
    else:
        form = BusinessRegistrationForm()
        partner_form = PartnershipDetailForm()
        company_form = CompanyDetailForm()

    return render(request, 'business/registration.html', {
        'form': form,
        'partner_form': partner_form,
        'company_form': company_form
    })


@login_required
def dashboard(request):
    businesses = Business.objects.filter(owner=request.user)
    total = businesses.count()
    approved = businesses.filter(status='approved').count()
    pending = businesses.filter(status='pending').count()
    context = {
        'businesses': businesses,
        'total': total,
        'approved': approved,
        'pending': pending,
    }
    return render(request, 'business/dashboard.html', context)