from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import BusinessRegistrationForm, PartnershipDetailForm, CompanyDetailForm
from .models import Business, PartnershipDetail, CompanyDetail
from django.forms import formset_factory
from django import forms
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

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

@login_required
def business_detail(request, business_id):
    business = get_object_or_404(Business, id=business_id, owner=request.user)

    partnership_detail = None
    company_detail = None

    if business.business_type == 'partnership':
        partnership_detail = PartnershipDetail.objects.filter(business=business).first()
    elif business.business_type == 'limited_company':
        company_detail = CompanyDetail.objects.filter(business=business).first()

    context = {
        'business': business,
        'partnership_detail': partnership_detail,
        'company_detail': company_detail,
    }
    return render(request, 'business/business_detail.html', context)

@login_required
def download_certificate(request, business_id):
    business = get_object_or_404(Business, id=business_id, owner=request.user)
    if not business.registration_certificate:
        raise Http404("Certificate not found.")

    return FileResponse(business.registration_certificate.open('rb'), as_attachment=True)