from django.urls import path
from .views import RegisterView, custom_login, profile_view, custom_logout, dashboard_view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/', dashboard_view, name='dashboard'),
]