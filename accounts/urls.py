from django.urls import path
from .views import RegisterView, custom_login, profile_view, custom_logout

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
]