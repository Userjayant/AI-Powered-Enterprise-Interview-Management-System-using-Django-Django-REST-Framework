"""
interviews/views.py
Interview Scheduling, Management & Feedback Views
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Interview, Feedback
from .forms import InterviewScheduleForm, InterviewUpdateForm, FeedbackForm
from candidates.models import Candidate

logger = logging.getLogger(__name__)


def send_interview_notification(interview, action='scheduled'):
    """Send email notification for interview events."""
    subject_map = {
        'scheduled': f'Interview Scheduled - {interview.get_round_type_display()}',
        'reminder': f'Interview Reminder - Tomorrow at {interview.scheduled_at.strftime("%I:%M %p")}',
        'cancelled': f'Interview Cancelled - {interview.get_round_type_display()}',
    }
    subject = subject_map.get(action, 'Interview Update')
    message = (
        f"Dear {interview.candidate.full_name},\n\n"
        f"Your {interview.get_round_type_display()} has been {action}.\n"
        f"Date & Time: {interview.scheduled_at.strftime('%d %B %Y at %I:%M %p')}\n"
        f"Duration: {interview.duration} minutes\n"
        f"Mode: {interview.get_mode_display()}\n"
    )
    if interview.meeting_link:
        message += f"Meeting Link: {interview.meeting_link}\n"
    if interview.location:
        message += f"Location: {interview.location}\n"
    message += "\nBest regards,\nHR Team"

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [interview.candidate.email])
        logger.info(f"Notification sent to {interview.candidate.email}")
    except Exception as e:
        logger.error(f"Email failed: {e}")


# ============================================================
# INTERVIEW VIEWS
# ============================================================

@method_decorator(login_required, name='dispatch')
class InterviewListView(View):
    template_name = 'interviews/interview_list.html'

    def get(self, request):
        # Interviewers see only their assigned interviews
        if request.user.is_interviewer:
            interviews = Interview.objects.filter(
                interviewer=request.user
            ).select_related('candidate', 'interviewer')
        elif request.user.is_candidate:
            try:
                interviews = Interview.objects.filter(
                    candidate=request.user.candidate_profile
                ).select_related('interviewer')
            except:
                interviews = Interview.objects.none()
        else:
            interviews = Interview.objects.all().select_related('candidate', 'interviewer')

        # Filters
        status = request.GET.get('status', '')
        round_type = request.GET.get('round', '')
        q = request.GET.get('q', '')

        if status:
            interviews = interviews.filter(status=status)
        if round_type:
            interviews = interviews.filter(round_type=round_type)
        if q and not request.user.is_candidate:
            interviews = interviews.filter(
                Q(candidate__full_name__icontains=q) |
                Q(interviewer__first_name__icontains=q)
            )

        paginator = Paginator(interviews, 10)
        page = paginator.get_page(request.GET.get('page'))

        return render(request, self.template_name, {
            'interviews': page,
            'status_choices': Interview.STATUS_CHOICES,
            'round_choices': Interview.ROUND_CHOICES,
            'filters': {'status': status, 'round': round_type, 'q': q},
            'upcoming_count': interviews.filter(
                status='scheduled', scheduled_at__gte=timezone.now()
            ).count() if hasattr(interviews, 'filter') else 0,
        })


@method_decorator(login_required, name='dispatch')
class InterviewScheduleView(View):
    template_name = 'interviews/schedule_interview.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_candidate:
            messages.error(request, 'Access denied.')
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = InterviewScheduleForm()
        candidate_id = request.GET.get('candidate')
        if candidate_id:
            try:
                candidate = Candidate.objects.get(pk=candidate_id)
                form.fields['candidate'].initial = candidate
            except Candidate.DoesNotExist:
                pass
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = InterviewScheduleForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.scheduled_by = request.user
            interview.save()
            # Update candidate status
            candidate = interview.candidate
            candidate.status = 'interview_scheduled'
            candidate.save()
            # Send notification
            send_interview_notification(interview, 'scheduled')
            messages.success(request, f'Interview scheduled for {interview.candidate.full_name}!')
            return redirect('interviews:detail', pk=interview.pk)
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class InterviewDetailView(View):
    template_name = 'interviews/interview_detail.html'

    def get(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)

        # Access control
        if request.user.is_candidate:
            try:
                if interview.candidate != request.user.candidate_profile:
                    messages.error(request, 'Access denied.')
                    return redirect('dashboard:home')
            except:
                messages.error(request, 'Access denied.')
                return redirect('dashboard:home')

        if request.user.is_interviewer and interview.interviewer != request.user:
            messages.error(request, 'Access denied.')
            return redirect('dashboard:home')

        feedback = None
        try:
            feedback = interview.feedback
        except Feedback.DoesNotExist:
            pass

        feedback_form = FeedbackForm()
        update_form = InterviewUpdateForm(instance=interview)

        return render(request, self.template_name, {
            'interview': interview,
            'feedback': feedback,
            'feedback_form': feedback_form,
            'update_form': update_form,
        })


@method_decorator(login_required, name='dispatch')
class InterviewUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_candidate:
            messages.error(request, 'Access denied.')
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)
        form = InterviewUpdateForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interview updated successfully!')
        else:
            messages.error(request, 'Please correct the errors.')
        return redirect('interviews:detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class InterviewDeleteView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_hr_admin:
            messages.error(request, 'Access denied.')
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)
        interview.delete()
        messages.success(request, 'Interview deleted.')
        return redirect('interviews:list')


# ============================================================
# FEEDBACK VIEWS
# ============================================================

@method_decorator(login_required, name='dispatch')
class FeedbackSubmitView(View):
    """Submit feedback for a completed interview."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_candidate:
            messages.error(request, 'Access denied.')
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, interview_pk):
        interview = get_object_or_404(Interview, pk=interview_pk)

        # Interviewers can only submit feedback for their own interviews
        if request.user.is_interviewer and interview.interviewer != request.user:
            messages.error(request, 'You can only submit feedback for your own interviews.')
            return redirect('interviews:detail', pk=interview_pk)

        # Check if feedback already exists
        if hasattr(interview, 'feedback'):
            messages.warning(request, 'Feedback already submitted for this interview.')
            return redirect('interviews:detail', pk=interview_pk)

        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.interview = interview
            feedback.submitted_by = request.user
            feedback.save()

            # Mark interview as completed
            interview.status = 'completed'
            interview.save()

            # Update candidate status
            candidate = interview.candidate
            candidate.status = 'interview_completed'
            candidate.save()

            messages.success(request, f'Feedback submitted! Overall Score: {feedback.overall_score}/10')
            return redirect('interviews:detail', pk=interview_pk)

        messages.error(request, 'Please correct the errors in the feedback form.')
        return redirect('interviews:detail', pk=interview_pk)


@method_decorator(login_required, name='dispatch')
class FeedbackDetailView(View):
    template_name = 'interviews/feedback_detail.html'

    def get(self, request, pk):
        feedback = get_object_or_404(Feedback, pk=pk)
        if request.user.is_candidate:
            messages.error(request, 'Access denied.')
            return redirect('dashboard:home')
        return render(request, self.template_name, {'feedback': feedback})
