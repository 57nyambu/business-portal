from business.models import Business
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils import timezone
User = get_user_model()

@login_required
def admin_dashboard(request):
      status_counts = Business.objects.values('status').annotate(count=Count('id'))
      status_map = {item['status']: item['count'] for item in status_counts}
      approved_count = status_map.get('approved', 0)
      rejected_count = status_map.get('rejected', 0)
      pending_count = status_map.get('pending', 0)

      user_count = User.objects.count()

      all_businesses = Business.objects.select_related('owner').all().order_by('-created_at')
      pending_businesses = Business.objects.filter(status='pending').order_by('-created_at')
      recent_approved_businesses = Business.objects.filter(
          status='approved',
          created_at__gte=timezone.now() - timedelta(days=7)
      ).order_by('-created_at')

      users = User.objects.all().order_by('-date_joined')

      recent_activity = [{
          'icon_bg': 'bg-blue-100',
          'icon_color': 'text-blue-600',
          'icon_svg': '<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />',
          'message': 'Admin dashboard loaded successfully',
          'meta': 'Just now'
      }]

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
      return render(request, 'management/addmin_dashboard.html', context)

def update_business_status(request, business_id):
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('landing')  # or wherever your non-admins should go

    business = get_object_or_404(Business, id=business_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'approved', 'rejected']:
            business.status = new_status
            business.save()
            messages.success(request, f"✅ Business '{business.name}' status updated to {new_status.upper()}.")
        else:
            messages.error(request, "Invalid status submitted.")

    return redirect('admin_dashboard')