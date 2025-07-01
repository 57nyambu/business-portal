from django.shortcuts import render
from business.models import Business
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from django.db.models import Count

def landing(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        try:
            # Get all business status counts in a single query
            status_counts = Business.objects.values('status').annotate(count=Count('id'))
            status_map = {item['status']: item['count'] for item in status_counts}
            
            approved_count = status_map.get('approved', 0)
            rejected_count = status_map.get('rejected', 0)
            pending_count = status_map.get('pending', 0)
            
            # Get all users count
            user_count = User.objects.count()
            
            # Get all pending businesses (no limit)
            pending_businesses = Business.objects.filter(status='pending').order_by('-created_at')
            
            # Get recently approved businesses (last 7 days)
            recent_approved_businesses = Business.objects.filter(
                status='approved',
                created_at__gte=timezone.now()-timedelta(days=7)
            ).order_by('-created_at')
            
            # Get ALL businesses ordered by creation date
            all_businesses = Business.objects.all().order_by('-created_at')
            
            # Get ALL users ordered by join date
            users = User.objects.all().order_by('-date_joined')
            
            # Sample activity data - replace with real activity logs if available
            recent_activity = [{
                'icon_bg': 'bg-blue-100',
                'icon_color': 'text-blue-600',
                'icon_svg': '<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />',
                'message': 'Admin dashboard loaded successfully',
                'meta': 'Just now'
            }]
            
            # Get county choices from model
            COUNTY_CHOICES = getattr(Business, 'COUNTY_CHOICES', [])
            
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
                'default_county': COUNTY_CHOICES[0][0] if COUNTY_CHOICES else '',
                'approval_days': 7,
                'notifications': True,
                'maintenance': False,
            }
            
            # Debug output to console to verify data
            print("\n=== ADMIN DASHBOARD DATA ===")
            print(f"Total Businesses: {Business.objects.count()}")
            print(f"- Approved: {approved_count}")
            print(f"- Pending: {pending_count}")
            print(f"- Rejected: {rejected_count}")
            print(f"Total Users: {user_count}")
            print(f"Pending Businesses Sample: {pending_businesses.count()} records")
            if pending_businesses.exists():
                print(f"First pending business: {pending_businesses.first().name} (Status: {pending_businesses.first().status})")
            print(f"All Businesses Sample: {all_businesses.count()} records")
            if all_businesses.exists():
                print(f"First business: {all_businesses.first().name} (Status: {all_businesses.first().status})")
            print(f"Users Sample: {users.count()} records")
            if users.exists():
                print(f"First user: {users.first().email}")
            print("===========================\n")
            
            return render(request, 'management/admin_dashboard.html', context)
            
        except Exception as e:
            print(f"\n!!! ERROR in admin dashboard: {str(e)}\n")
            # Fallback to empty context if there's an error
            return render(request, 'management/admin_dashboard.html', {
                'approved_count': 0,
                'pending_count': 0,
                'rejected_count': 0,
                'user_count': 0,
                'recent_activity': [],
                'pending_businesses': [],
                'recent_approved_businesses': [],
                'all_businesses': [],
                'users': [],
                'COUNTY_CHOICES': [],
            })
    
    return render(request, 'core/landing.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def services(request):
    return render(request, 'core/services.html')

def pricing(request):
    return render(request, 'core/pricing.html')