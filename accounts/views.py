from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import UserRegistrationForm

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/accounts/login/'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

def custom_login(request):
    if request.method == 'POST':
        # Handle login logic (using Django's built-in auth)
        pass
    return render(request, 'accounts/login.html')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

def custom_logout(request):
    logout(request)
    return redirect('landing')