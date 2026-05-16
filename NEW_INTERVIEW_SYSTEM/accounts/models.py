"""
accounts/models.py
Custom User Model with Role-based Access Control
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


def user_profile_path(instance, filename):
    """Dynamic upload path for profile images."""
    return f'profiles/{instance.username}/{filename}'


class User(AbstractUser):
    """
    Extended User model with role-based access.
    Roles: hr_admin, interviewer, candidate
    """

    ROLE_CHOICES = [
        ('hr_admin', 'HR Admin'),
        ('interviewer', 'Interviewer'),
        ('candidate', 'Candidate'),
    ]

    DEPARTMENT_CHOICES = [
        ('engineering', 'Engineering'),
        ('product', 'Product'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('hr', 'Human Resources'),
        ('finance', 'Finance'),
        ('operations', 'Operations'),
        ('other', 'Other'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    profile_image = models.ImageField(upload_to=user_profile_path, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True)
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_hr_admin(self):
        return self.role == 'hr_admin'

    @property
    def is_interviewer(self):
        return self.role == 'interviewer'

    @property
    def is_candidate(self):
        return self.role == 'candidate'

    def get_dashboard_url(self):
        """Return role-specific dashboard URL."""
        from django.urls import reverse
        return reverse('dashboard:home')

    def get_initials(self):
        """Return user initials for avatar fallback."""
        parts = self.get_full_name().split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        elif parts:
            return parts[0][0].upper()
        return self.email[0].upper()
