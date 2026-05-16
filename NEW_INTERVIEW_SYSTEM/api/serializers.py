"""
api/serializers.py
DRF Serializers for all models
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from candidates.models import Candidate, JobRole
from interviews.models import Interview, Feedback

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name',
                  'role', 'department', 'phone_number', 'is_verified']
        read_only_fields = ['id', 'email']

    def get_full_name(self, obj):
        return obj.get_full_name()


class JobRoleSerializer(serializers.ModelSerializer):
    skills_list = serializers.SerializerMethodField()
    candidate_count = serializers.SerializerMethodField()

    class Meta:
        model = JobRole
        fields = ['id', 'title', 'department', 'required_skills', 'skills_list',
                  'job_description', 'minimum_experience', 'is_active',
                  'candidate_count', 'created_at']

    def get_skills_list(self, obj):
        return obj.get_skills_list()

    def get_candidate_count(self, obj):
        return obj.candidates.count()


class CandidateListSerializer(serializers.ModelSerializer):
    applied_role_title = serializers.CharField(source='applied_role.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'full_name', 'email', 'phone', 'applied_role',
                  'applied_role_title', 'experience', 'ai_resume_score',
                  'status', 'status_display', 'created_at']


class CandidateDetailSerializer(serializers.ModelSerializer):
    applied_role = JobRoleSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    skills_list = serializers.SerializerMethodField()
    interview_count = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = '__all__'

    def get_skills_list(self, obj):
        return obj.get_skills_list()

    def get_interview_count(self, obj):
        return obj.interviews.count()


class FeedbackSerializer(serializers.ModelSerializer):
    recommendation_display = serializers.CharField(source='get_recommendation_display', read_only=True)
    submitted_by_name = serializers.CharField(source='submitted_by.get_full_name', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'interview', 'technical_score', 'communication_score',
                  'problem_solving_score', 'confidence_score', 'overall_score',
                  'strengths', 'weaknesses', 'comments', 'recommendation',
                  'recommendation_display', 'submitted_by_name', 'created_at']
        read_only_fields = ['overall_score']


class InterviewListSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.full_name', read_only=True)
    interviewer_name = serializers.CharField(source='interviewer.get_full_name', read_only=True)
    round_display = serializers.CharField(source='get_round_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    has_feedback = serializers.SerializerMethodField()

    class Meta:
        model = Interview
        fields = ['id', 'candidate', 'candidate_name', 'interviewer', 'interviewer_name',
                  'round_type', 'round_display', 'scheduled_at', 'duration', 'mode',
                  'status', 'status_display', 'has_feedback']

    def get_has_feedback(self, obj):
        return obj.has_feedback()


class InterviewDetailSerializer(serializers.ModelSerializer):
    candidate = CandidateListSerializer(read_only=True)
    interviewer = UserSerializer(read_only=True)
    feedback = FeedbackSerializer(read_only=True)
    round_display = serializers.CharField(source='get_round_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Interview
        fields = '__all__'


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard analytics API."""
    total_candidates = serializers.IntegerField()
    selected = serializers.IntegerField()
    rejected = serializers.IntegerField()
    active_roles = serializers.IntegerField()
    upcoming_interviews = serializers.IntegerField()
    conversion_rate = serializers.FloatField()
