from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import UserRegistrationForm, CustomAuthenticationForm
from django.urls import reverse_lazy

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('landing')  # Redirect to homepage (change 'landing' to your homepage url name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_register_page'] = True
        return context

    def form_valid(self, form):
        user = form.save()
        authenticated_user = authenticate(
            self.request,
            username=user.email,
            password=form.cleaned_data['password1']
        )
        if authenticated_user is not None:
            login(self.request, authenticated_user)
            messages.success(self.request, "Registration successful! Welcome!")
        else:
            messages.error(self.request, "Registration successful, but automatic login failed. Please log in manually.")
        return redirect(self.success_url)  # Will now redirect to homepage

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form, 'is_login_page': True})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def dashboard_view(request):
    return render(request, 'business/dashboard.html', {'user': request.user})

def custom_logout(request):
    logout(request)
    return redirect('landing')