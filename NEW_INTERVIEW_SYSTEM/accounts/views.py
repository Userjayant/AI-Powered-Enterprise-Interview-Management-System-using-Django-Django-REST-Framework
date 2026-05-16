"""
accounts/views.py
Authentication Views - Login, Register, Profile, Logout
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Q

from .forms import CustomLoginForm, CandidateRegistrationForm, StaffRegistrationForm, UserProfileForm

User = get_user_model()
logger = logging.getLogger(__name__)


class LoginView(View):
    """Email-based login with role-based redirect."""
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        form = CustomLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            logger.info(f"User {user.email} logged in successfully.")
            messages.success(request, f'Welcome back, {user.get_full_name() or user.email}!')
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
        messages.error(request, 'Invalid email or password. Please try again.')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Logout and redirect to login."""

    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('accounts:login')


class CandidateRegisterView(View):
    """Candidate self-registration."""
    template_name = 'accounts/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        form = CandidateRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the platform.')
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """User profile view and update."""
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form, 'user_obj': request.user})

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form, 'user_obj': request.user})


@method_decorator(login_required, name='dispatch')
class StaffCreateView(View):
    """HR Admin creates staff (interviewer/HR) accounts."""
    template_name = 'accounts/create_staff.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_hr_admin:
            messages.error(request, 'Access denied. HR Admin privileges required.')
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = StaffRegistrationForm()
        staff_list = User.objects.filter(role__in=['hr_admin', 'interviewer']).order_by('-date_joined')
        return render(request, self.template_name, {'form': form, 'staff_list': staff_list})

    def post(self, request):
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Staff account created for {user.get_full_name()}!')
            return redirect('accounts:create_staff')
        staff_list = User.objects.filter(role__in=['hr_admin', 'interviewer']).order_by('-date_joined')
        return render(request, self.template_name, {'form': form, 'staff_list': staff_list})
