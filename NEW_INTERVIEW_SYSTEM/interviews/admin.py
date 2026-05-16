"""interviews/admin.py"""
from django.contrib import admin
from .models import Interview, Feedback


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'interviewer', 'round_type', 'scheduled_at', 'status', 'mode']
    list_filter = ['status', 'round_type', 'mode']
    search_fields = ['candidate__full_name', 'interviewer__email']
    date_hierarchy = 'scheduled_at'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['interview', 'overall_score', 'recommendation', 'submitted_by', 'created_at']
    list_filter = ['recommendation']
    readonly_fields = ['overall_score', 'created_at']
