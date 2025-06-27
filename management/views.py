from django.shortcuts import render

def admin_dashboard(request):
  return render(request, 'management/admin_dashboard.html')