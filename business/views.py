from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import BusinessRegistrationForm, PartnershipDetailForm, CompanyDetailForm
from .models import Business
from django.forms import formset_factory
from django import forms

@login_required
def register_business(request):
    if request.method == 'POST':
        form = BusinessRegistrationForm(request.POST, request.FILES)
        business_type = request.POST.get('business_type')
        partnership_form = PartnershipDetailForm(request.POST, prefix='partnership')
        company_form = CompanyDetailForm(request.POST, prefix='company')

        valid = form.is_valid()
        if business_type == 'partnership':
            valid = valid and partnership_form.is_valid()
        elif business_type == 'company':
            valid = valid and company_form.is_valid()

        if valid:
            business = form.save(commit=False)
            business.owner = request.user
            business.save()

            if business_type == 'partnership':
                partnership = partnership_form.save(commit=False)
                partnership.business = business
                partnership.save()
            elif business_type == 'company':
                company = company_form.save(commit=False)
                company.business = business
                company.save()

            return redirect('/business/dashboard/')
    else:
        form = BusinessRegistrationForm()
        partnership_form = PartnershipDetailForm(prefix='partnership')
        company_form = CompanyDetailForm(prefix='company')

    return render(request, 'business/registration.html', {
        'form': form,
        'partnership_form': partnership_form,
        'company_form': company_form,
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