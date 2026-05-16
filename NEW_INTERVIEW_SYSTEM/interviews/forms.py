"""
interviews/forms.py
Interview Scheduling & Feedback Forms
"""

from django import forms
from django.contrib.auth import get_user_model
from .models import Interview, Feedback
from candidates.models import Candidate

User = get_user_model()


class InterviewScheduleForm(forms.ModelForm):
    """Schedule a new interview."""

    scheduled_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Interview
        fields = [
            'candidate', 'interviewer', 'round_type', 'scheduled_at',
            'duration', 'mode', 'meeting_link', 'location', 'notes'
        ]
        widgets = {
            'candidate': forms.Select(attrs={'class': 'form-select'}),
            'interviewer': forms.Select(attrs={'class': 'form-select'}),
            'round_type': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'step': 15}),
            'mode': forms.Select(attrs={'class': 'form-select'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://meet.google.com/...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Office address or room'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['interviewer'].queryset = User.objects.filter(
            role__in=['interviewer', 'hr_admin']
        ).order_by('first_name')
        self.fields['candidate'].queryset = Candidate.objects.filter(
            status__in=['applied', 'screening', 'shortlisted', 'interview_scheduled']
        ).order_by('full_name')


class InterviewUpdateForm(forms.ModelForm):
    """Update interview status and details."""

    scheduled_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Interview
        fields = ['scheduled_at', 'duration', 'mode', 'meeting_link', 'location', 'status', 'notes']
        widgets = {
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'mode': forms.Select(attrs={'class': 'form-select'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FeedbackForm(forms.ModelForm):
    """Interviewer feedback submission."""

    class Meta:
        model = Feedback
        fields = [
            'technical_score', 'communication_score',
            'problem_solving_score', 'confidence_score',
            'strengths', 'weaknesses', 'comments', 'recommendation'
        ]
        widgets = {
            'technical_score': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0, 'max': 10, 'step': 0.5
            }),
            'communication_score': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0, 'max': 10, 'step': 0.5
            }),
            'problem_solving_score': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0, 'max': 10, 'step': 0.5
            }),
            'confidence_score': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0, 'max': 10, 'step': 0.5
            }),
            'strengths': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Key strengths observed...'}),
            'weaknesses': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Areas of improvement...'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed evaluation comments...'}),
            'recommendation': forms.Select(attrs={'class': 'form-select'}),
        }
