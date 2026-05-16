"""candidates/admin.py"""
from django.contrib import admin
from .models import JobRole, Candidate


@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'minimum_experience', 'is_active', 'created_at']
    list_filter = ['is_active', 'department']
    search_fields = ['title', 'department', 'required_skills']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'applied_role', 'experience', 'ai_resume_score', 'status', 'created_at']
    list_filter = ['status', 'applied_role']
    search_fields = ['full_name', 'email', 'skills', 'current_company']
    readonly_fields = ['ai_resume_score', 'created_at', 'updated_at']
