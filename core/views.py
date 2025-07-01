from django.shortcuts import render
from business.models import Business
from django.utils import timezone
from datetime import timedelta
from accounts.models import User

def landing(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        # Add debug prints to see what data is actually being retrieved
        print("=== DEBUG: Admin Dashboard Data ===")
        
        # Check total counts first
        total_businesses = Business.objects.count()
        total_users = User.objects.count()
        print(f"Total businesses in database: {total_businesses}")
        print(f"Total users in database: {total_users}")
        
        # Check what status values actually exist
        actual_statuses = list(Business.objects.values_list('status', flat=True).distinct())
        print(f"Actual status values in database: {actual_statuses}")
        
        # Check STATUS_CHOICES from model
        try:
            status_choices = Business.STATUS_CHOICES
            print(f"STATUS_CHOICES from model: {status_choices}")
        except AttributeError:
            print("Business model doesn't have STATUS_CHOICES attribute")
        
        # Get counts with debug info
        approved_count = Business.objects.filter(status='approved').count()
        rejected_count = Business.objects.filter(status='rejected').count()
        pending_count = Business.objects.filter(status='pending').count()
        user_count = User.objects.count()
        
        print(f"Approved businesses: {approved_count}")
        print(f"Rejected businesses: {rejected_count}")
        print(f"Pending businesses: {pending_count}")
        print(f"User count: {user_count}")
        
        # Check if the counts add up
        calculated_total = approved_count + rejected_count + pending_count
        print(f"Sum of status counts: {calculated_total} (should equal total: {total_businesses})")
        
        # Sample business data
        if total_businesses > 0:
            sample_business = Business.objects.first()
            print(f"Sample business:")
            print(f"  - Name: {sample_business.name}")
            print(f"  - Status: '{sample_business.status}'")
            print(f"  - Business Type: {sample_business.business_type}")
            print(f"  - County: {sample_business.county}")
            print(f"  - Created: {sample_business.created_at}")
            print(f"  - Has get_business_type_display: {hasattr(sample_business, 'get_business_type_display')}")
            print(f"  - Has get_county_display: {hasattr(sample_business, 'get_county_display')}")
            
            # Test the display methods
            try:
                print(f"  - Business type display: {sample_business.get_business_type_display()}")
            except Exception as e:
                print(f"  - Error getting business type display: {e}")
            
            try:
                print(f"  - County display: {sample_business.get_county_display()}")
            except Exception as e:
                print(f"  - Error getting county display: {e}")
        
        # Sample user data
        if total_users > 0:
            sample_user = User.objects.first()
            print(f"Sample user:")
            print(f"  - Username: {sample_user.username}")
            print(f"  - Email: {sample_user.email}")
            print(f"  - Full name: {sample_user.get_full_name()}")
            print(f"  - Is staff: {sample_user.is_staff}")
            print(f"  - Is active: {sample_user.is_active}")
        
        # Get querysets for template
        pending_businesses = Business.objects.filter(status='pending')
        recent_approved_businesses = Business.objects.filter(
            status='approved', 
            created_at__gte=timezone.now()-timedelta(days=7)
        )
        all_businesses = Business.objects.all()
        users = User.objects.all()
        
        print(f"Pending businesses queryset count: {pending_businesses.count()}")
        print(f"Recent approved businesses queryset count: {recent_approved_businesses.count()}")
        print(f"All businesses queryset count: {all_businesses.count()}")
        print(f"Users queryset count: {users.count()}")
        
        # Test if querysets are actually populated
        print("First 3 pending businesses:")
        for i, business in enumerate(pending_businesses[:3]):
            print(f"  {i+1}. {business.name} - {business.status}")
        
        print("First 3 users:")
        for i, user in enumerate(users[:3]):
            print(f"  {i+1}. {user.username} - {user.get_full_name()}")
        
        # Populate recent activity (example)
        recent_activity = [
            {
                'icon_bg': 'bg-blue-100',
                'icon_color': 'text-blue-600',
                'icon_svg': '<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />',
                'message': f'New business registration: "Test Business"',
                'meta': '2 hours ago'
            },
        ]
        
        # Check COUNTY_CHOICES
        try:
            COUNTY_CHOICES = getattr(Business, 'COUNTY_CHOICES', [])
            print(f"COUNTY_CHOICES available: {len(COUNTY_CHOICES)} choices")
            if COUNTY_CHOICES:
                print(f"First 3 county choices: {COUNTY_CHOICES[:3]}")
        except Exception as e:
            print(f"Error getting COUNTY_CHOICES: {e}")
            COUNTY_CHOICES = []
        
        context = {
            'approved_count': approved_count,
            'pending_count': pending_count,
            'rejected_count': rejected_count,
            'user_count': user_count,
            'recent_activity': recent_activity,
            'pending_businesses': pending_businesses,
            'recent_approved_businesses': recent_approved_businesses,
            'all_businesses': all_businesses,
            'users': users,
            'COUNTY_CHOICES': COUNTY_CHOICES,
            'business_prefix': 'BRP',
            'default_county': '047',
            'approval_days': 7,
            'notifications': True,
            'maintenance': False,
        }
        
        print("=== Final Context Summary ===")
        print(f"Context keys: {list(context.keys())}")
        print("=== End Debug ===")
        
        return render(request, 'management/admin_dashboard.html', context)
    return render(request, 'core/landing.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def services(request):
    return render(request, 'core/services.html')

def pricing(request):
    return render(request, 'core/pricing.html')