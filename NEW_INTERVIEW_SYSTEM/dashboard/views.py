"""
dashboard/views.py
Role-based Dashboard with Analytics
"""

import json
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from django.db.models import Count, Avg, Q
from datetime import timedelta

from candidates.models import Candidate, JobRole
from interviews.models import Interview, Feedback

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class DashboardHomeView(View):
    """Main dashboard - renders different content by role."""

    def get(self, request):
        user = request.user

        if user.is_hr_admin:
            return self._hr_dashboard(request)
        elif user.is_interviewer:
            return self._interviewer_dashboard(request)
        else:
            return self._candidate_dashboard(request)

    def _hr_dashboard(self, request):
        """HR Admin analytics dashboard."""
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)

        # Core stats
        total_candidates = Candidate.objects.count()
        selected = Candidate.objects.filter(status='selected').count()
        rejected = Candidate.objects.filter(status='rejected').count()
        active_roles = JobRole.objects.filter(is_active=True).count()
        upcoming_interviews = Interview.objects.filter(
            status='scheduled', scheduled_at__gte=now
        ).count()
        pending_feedback = Interview.objects.filter(
            status='completed'
        ).exclude(feedback__isnull=False).count()

        # Pipeline breakdown
        pipeline = Candidate.objects.values('status').annotate(count=Count('id'))
        pipeline_data = {item['status']: item['count'] for item in pipeline}

        # Monthly trend (last 6 months)
        monthly_data = []
        monthly_labels = []
        for i in range(5, -1, -1):
            month_start = (now - timedelta(days=30 * i)).replace(day=1, hour=0, minute=0, second=0)
            month_end = (month_start + timedelta(days=32)).replace(day=1)
            count = Candidate.objects.filter(
                created_at__gte=month_start, created_at__lt=month_end
            ).count()
            monthly_data.append(count)
            monthly_labels.append(month_start.strftime('%b %Y'))

        # Department-wise distribution
        dept_data = Candidate.objects.filter(
            applied_role__isnull=False
        ).values('applied_role__department').annotate(
            count=Count('id')
        ).order_by('-count')[:6]

        # Recent candidates
        recent_candidates = Candidate.objects.select_related(
            'applied_role'
        ).order_by('-created_at')[:8]

        # Upcoming interviews
        upcoming = Interview.objects.filter(
            status='scheduled', scheduled_at__gte=now
        ).select_related('candidate', 'interviewer').order_by('scheduled_at')[:5]

        # Top scored candidates
        top_candidates = Candidate.objects.filter(
            ai_resume_score__gt=0
        ).order_by('-ai_resume_score')[:5]

        # Conversion rate
        conversion_rate = round((selected / total_candidates * 100), 1) if total_candidates > 0 else 0
        rejection_rate = round((rejected / total_candidates * 100), 1) if total_candidates > 0 else 0

        context = {
            'total_candidates': total_candidates,
            'selected': selected,
            'rejected': rejected,
            'active_roles': active_roles,
            'upcoming_interviews': upcoming_interviews,
            'pending_feedback': pending_feedback,
            'conversion_rate': conversion_rate,
            'rejection_rate': rejection_rate,
            'pipeline_data': json.dumps(pipeline_data),
            'monthly_labels': json.dumps(monthly_labels),
            'monthly_data': json.dumps(monthly_data),
            'dept_labels': json.dumps([d['applied_role__department'] for d in dept_data]),
            'dept_counts': json.dumps([d['count'] for d in dept_data]),
            'recent_candidates': recent_candidates,
            'upcoming': upcoming,
            'top_candidates': top_candidates,
        }
        return render(request, 'dashboard/hr_dashboard.html', context)

    def _interviewer_dashboard(self, request):
        """Interviewer-specific dashboard."""
        now = timezone.now()
        user = request.user

        my_interviews = Interview.objects.filter(
            interviewer=user
        ).select_related('candidate', 'candidate__applied_role')

        upcoming = my_interviews.filter(
            status='scheduled', scheduled_at__gte=now
        ).order_by('scheduled_at')[:5]

        completed = my_interviews.filter(status='completed').count()
        pending_feedback = my_interviews.filter(
            status='completed'
        ).exclude(feedback__isnull=False).count()
        total_assigned = my_interviews.count()

        today_interviews = my_interviews.filter(
            scheduled_at__date=now.date(), status='scheduled'
        )

        recent_feedback = Feedback.objects.filter(
            submitted_by=user
        ).select_related(
            'interview__candidate'
        ).order_by('-created_at')[:5]

        avg_score = Feedback.objects.filter(
            submitted_by=user
        ).aggregate(avg=Avg('overall_score'))['avg']

        context = {
            'upcoming': upcoming,
            'completed': completed,
            'pending_feedback': pending_feedback,
            'total_assigned': total_assigned,
            'today_interviews': today_interviews,
            'recent_feedback': recent_feedback,
            'avg_score': round(avg_score, 1) if avg_score else 0,
        }
        return render(request, 'dashboard/interviewer_dashboard.html', context)

    def _candidate_dashboard(self, request):
        """Candidate personal dashboard."""
        candidate = None
        interviews = []
        feedback_list = []

        try:
            candidate = request.user.candidate_profile
            interviews = Interview.objects.filter(
                candidate=candidate
            ).select_related('interviewer').order_by('-scheduled_at')

            feedback_list = Feedback.objects.filter(
                interview__candidate=candidate
            ).select_related('interview')
        except Exception:
            pass

        context = {
            'candidate': candidate,
            'interviews': interviews,
            'feedback_list': feedback_list,
            'total_interviews': len(interviews),
            'completed_interviews': sum(1 for i in interviews if i.status == 'completed'),
        }
        return render(request, 'dashboard/candidate_dashboard.html', context)
