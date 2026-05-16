"""
interviews/models.py
Interview Scheduling & Feedback Models
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Interview(models.Model):
    """Interview session linking candidate, interviewer, round."""

    ROUND_CHOICES = [
        ('screening', 'HR Screening'),
        ('technical_1', 'Technical Round 1'),
        ('technical_2', 'Technical Round 2'),
        ('system_design', 'System Design'),
        ('managerial', 'Managerial Round'),
        ('hr_final', 'HR Final Round'),
        ('cultural_fit', 'Cultural Fit'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
        ('no_show', 'No Show'),
    ]

    MODE_CHOICES = [
        ('online', 'Online (Video Call)'),
        ('phone', 'Phone Call'),
        ('in_person', 'In Person'),
    ]

    candidate = models.ForeignKey(
        'candidates.Candidate',
        on_delete=models.CASCADE,
        related_name='interviews'
    )
    interviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_interviews'
    )
    scheduled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='scheduled_interviews'
    )
    round_type = models.CharField(max_length=30, choices=ROUND_CHOICES)
    scheduled_at = models.DateTimeField()
    duration = models.PositiveIntegerField(default=60, help_text='Duration in minutes')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='online')
    meeting_link = models.URLField(blank=True)
    location = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, help_text='Internal notes for interviewer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_at']
        verbose_name = 'Interview'
        verbose_name_plural = 'Interviews'

    def __str__(self):
        return f"{self.candidate.full_name} - {self.get_round_type_display()} ({self.scheduled_at.strftime('%d %b %Y')})"

    def get_status_badge(self):
        badge_map = {
            'scheduled': 'bg-primary',
            'in_progress': 'bg-warning text-dark',
            'completed': 'bg-success',
            'cancelled': 'bg-danger',
            'rescheduled': 'bg-info',
            'no_show': 'bg-secondary',
        }
        return badge_map.get(self.status, 'bg-secondary')

    def has_feedback(self):
        return hasattr(self, 'feedback')


class Feedback(models.Model):
    """Detailed interview feedback and scoring."""

    RECOMMENDATION_CHOICES = [
        ('strong_hire', 'Strong Hire'),
        ('hire', 'Hire'),
        ('maybe', 'Maybe'),
        ('no_hire', 'No Hire'),
        ('strong_no_hire', 'Strong No Hire'),
    ]

    interview = models.OneToOneField(
        Interview,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    # Scores out of 10
    technical_score = models.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    communication_score = models.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    problem_solving_score = models.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    confidence_score = models.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    overall_score = models.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True, blank=True
    )

    strengths = models.TextField()
    weaknesses = models.TextField()
    comments = models.TextField()
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback Records'

    def __str__(self):
        return f"Feedback: {self.interview} - {self.get_recommendation_display()}"

    def save(self, *args, **kwargs):
        # Auto-calculate overall score as weighted average
        self.overall_score = round(
            (float(self.technical_score) * 0.4 +
             float(self.communication_score) * 0.2 +
             float(self.problem_solving_score) * 0.3 +
             float(self.confidence_score) * 0.1), 1
        )
        super().save(*args, **kwargs)

    def get_recommendation_badge(self):
        badge_map = {
            'strong_hire': 'bg-success',
            'hire': 'bg-primary',
            'maybe': 'bg-warning text-dark',
            'no_hire': 'bg-danger',
            'strong_no_hire': 'bg-danger',
        }
        return badge_map.get(self.recommendation, 'bg-secondary')

    def score_percentage(self):
        return round(float(self.overall_score) * 10, 1) if self.overall_score else 0
