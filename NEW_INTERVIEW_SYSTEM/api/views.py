"""
api/views.py
DRF ViewSets for all models
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count, Avg

from candidates.models import Candidate, JobRole
from interviews.models import Interview, Feedback
from .serializers import (
    CandidateListSerializer, CandidateDetailSerializer,
    JobRoleSerializer, InterviewListSerializer, InterviewDetailSerializer,
    FeedbackSerializer, DashboardStatsSerializer, UserSerializer
)


class JobRoleViewSet(viewsets.ModelViewSet):
    queryset = JobRole.objects.all()
    serializer_class = JobRoleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'department']
    search_fields = ['title', 'department', 'required_skills']
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def candidates(self, request, pk=None):
        role = self.get_object()
        candidates = role.candidates.all()
        serializer = CandidateListSerializer(candidates, many=True)
        return Response(serializer.data)


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.select_related('applied_role').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'applied_role']
    search_fields = ['full_name', 'email', 'skills', 'current_company']
    ordering_fields = ['created_at', 'ai_resume_score', 'experience']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CandidateDetailSerializer
        return CandidateListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_candidate:
            try:
                return Candidate.objects.filter(user=user)
            except:
                return Candidate.objects.none()
        return super().get_queryset()

    @action(detail=True, methods=['post'])
    def compute_score(self, request, pk=None):
        candidate = self.get_object()
        score = candidate.compute_ai_score()
        candidate.ai_resume_score = score
        candidate.save()
        return Response({'score': float(score), 'message': f'Score updated to {score}'})

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        candidate = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Candidate.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        candidate.status = new_status
        candidate.remarks = request.data.get('remarks', candidate.remarks)
        candidate.save()
        return Response({'status': candidate.status, 'message': 'Status updated'})


class InterviewViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'round_type', 'mode']
    search_fields = ['candidate__full_name', 'interviewer__email']
    ordering_fields = ['scheduled_at']

    def get_queryset(self):
        user = self.request.user
        qs = Interview.objects.select_related('candidate', 'interviewer')
        if user.is_interviewer:
            return qs.filter(interviewer=user)
        if user.is_candidate:
            try:
                return qs.filter(candidate=user.candidate_profile)
            except:
                return Interview.objects.none()
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InterviewDetailSerializer
        return InterviewListSerializer

    def perform_create(self, serializer):
        serializer.save(scheduled_by=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        upcoming = self.get_queryset().filter(
            status='scheduled', scheduled_at__gte=timezone.now()
        ).order_by('scheduled_at')[:10]
        serializer = InterviewListSerializer(upcoming, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = self.get_queryset().filter(
            scheduled_at__date=timezone.now().date()
        )
        serializer = InterviewListSerializer(today, many=True)
        return Response(serializer.data)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('interview__candidate', 'submitted_by').all()
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_interviewer:
            return self.queryset.filter(submitted_by=user)
        if user.is_candidate:
            try:
                return self.queryset.filter(interview__candidate=user.candidate_profile)
            except:
                return Feedback.objects.none()
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)


class DashboardStatsViewSet(viewsets.ViewSet):
    """Analytics stats endpoint for HR dashboard."""

    def list(self, request):
        if not request.user.is_hr_admin:
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        from candidates.models import Candidate, JobRole
        from interviews.models import Interview

        total = Candidate.objects.count()
        selected = Candidate.objects.filter(status='selected').count()
        rejected = Candidate.objects.filter(status='rejected').count()
        active_roles = JobRole.objects.filter(is_active=True).count()
        upcoming = Interview.objects.filter(
            status='scheduled', scheduled_at__gte=timezone.now()
        ).count()
        conversion = round((selected / total * 100), 1) if total > 0 else 0

        data = {
            'total_candidates': total,
            'selected': selected,
            'rejected': rejected,
            'active_roles': active_roles,
            'upcoming_interviews': upcoming,
            'conversion_rate': conversion,
        }
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)
