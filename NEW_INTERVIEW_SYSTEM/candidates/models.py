"""
candidates/models.py
JobRole and Candidate Models with AI Resume Scoring
"""

from django.db import models
from django.conf import settings
import re


class JobRole(models.Model):
    """Job opening / position definition."""

    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    required_skills = models.TextField(help_text='Comma-separated skills')
    job_description = models.TextField()
    minimum_experience = models.PositiveIntegerField(default=0, help_text='Years')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        related_name='created_roles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job Role'
        verbose_name_plural = 'Job Roles'

    def __str__(self):
        return f"{self.title} - {self.department}"

    def get_skills_list(self):
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]


def resume_upload_path(instance, filename):
    return f'resumes/{instance.user.email}/{filename}'


class Candidate(models.Model):
    """Candidate profile with hiring pipeline tracking."""

    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interview_completed', 'Interview Completed'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('on_hold', 'On Hold'),
        ('withdrawn', 'Withdrawn'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='candidate_profile',
        null=True, blank=True
    )
    applied_role = models.ForeignKey(
        JobRole, on_delete=models.SET_NULL,
        null=True, related_name='candidates'
    )
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    resume = models.FileField(upload_to=resume_upload_path, blank=True, null=True)
    skills = models.TextField(help_text='Comma-separated skills', blank=True)
    experience = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    current_company = models.CharField(max_length=200, blank=True)
    current_ctc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_ctc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notice_period = models.PositiveIntegerField(default=0, help_text='Days')
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    ai_resume_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='applied')
    remarks = models.TextField(blank=True)
    source = models.CharField(max_length=100, blank=True, help_text='How did they find us?')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f"{self.full_name} - {self.applied_role}"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def compute_ai_score(self):
        """
        AI Resume Score: keyword matching + experience weighting.
        Returns a score 0-100.
        """
        if not self.applied_role:
            return 0

        score = 0
        required = [s.lower() for s in self.applied_role.get_skills_list()]
        candidate_skills = [s.lower() for s in self.get_skills_list()]

        # Skill match (60 points max)
        if required:
            matched = sum(1 for s in required if s in candidate_skills)
            skill_score = (matched / len(required)) * 60
            score += skill_score

        # Experience match (25 points max)
        min_exp = self.applied_role.minimum_experience
        if min_exp > 0:
            exp_ratio = min(float(self.experience) / min_exp, 1.5)
            exp_score = min(exp_ratio * 25, 25)
        else:
            exp_score = 25 if self.experience >= 0 else 0
        score += exp_score

        # Profile completeness bonus (15 points)
        if self.linkedin_profile:
            score += 5
        if self.github_profile:
            score += 5
        if self.resume:
            score += 5

        return round(min(score, 100), 2)

    def get_status_badge_class(self):
        badge_map = {
            'applied': 'bg-secondary',
            'screening': 'bg-info',
            'shortlisted': 'bg-primary',
            'interview_scheduled': 'bg-warning text-dark',
            'interview_completed': 'bg-light text-dark border',
            'selected': 'bg-success',
            'rejected': 'bg-danger',
            'on_hold': 'bg-warning text-dark',
            'withdrawn': 'bg-secondary',
        }
        return badge_map.get(self.status, 'bg-secondary')
