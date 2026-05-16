"""
candidates/forms.py
Candidate and JobRole Forms
"""

from django import forms
from .models import Candidate, JobRole


class JobRoleForm(forms.ModelForm):
    class Meta:
        model = JobRole
        fields = ['title', 'department', 'required_skills', 'job_description', 'minimum_experience', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Python Developer'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Engineering'}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, REST API, PostgreSQL'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'minimum_experience': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'full_name', 'email', 'phone', 'applied_role', 'resume',
            'skills', 'experience', 'current_company', 'current_ctc',
            'expected_ctc', 'notice_period', 'linkedin_profile',
            'github_profile', 'status', 'source', 'remarks'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'applied_role': forms.Select(attrs={'class': 'form-select'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, SQL'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': 0}),
            'current_company': forms.TextInput(attrs={'class': 'form-control'}),
            'current_ctc': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Annual CTC in LPA'}),
            'expected_ctc': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Expected CTC in LPA'}),
            'notice_period': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Days'}),
            'linkedin_profile': forms.URLInput(attrs={'class': 'form-control'}),
            'github_profile': forms.URLInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn, Referral, Job Portal'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applied_role'].queryset = JobRole.objects.filter(is_active=True)


class CandidateSelfUpdateForm(forms.ModelForm):
    """Form for candidates to update their own profile."""
    class Meta:
        model = Candidate
        fields = ['phone', 'resume', 'skills', 'experience', 'current_company',
                  'current_ctc', 'expected_ctc', 'notice_period', 'linkedin_profile', 'github_profile']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, SQL'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': 0}),
            'current_company': forms.TextInput(attrs={'class': 'form-control'}),
            'current_ctc': forms.NumberInput(attrs={'class': 'form-control'}),
            'expected_ctc': forms.NumberInput(attrs={'class': 'form-control'}),
            'notice_period': forms.NumberInput(attrs={'class': 'form-control'}),
            'linkedin_profile': forms.URLInput(attrs={'class': 'form-control'}),
            'github_profile': forms.URLInput(attrs={'class': 'form-control'}),
        }


class CandidateStatusForm(forms.ModelForm):
    """Quick status update form."""
    class Meta:
        model = Candidate
        fields = ['status', 'remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
