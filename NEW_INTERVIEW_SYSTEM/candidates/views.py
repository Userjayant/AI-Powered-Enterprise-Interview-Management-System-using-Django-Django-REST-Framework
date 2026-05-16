"""
candidates/views.py
Candidate and JobRole Management Views
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from .models import Candidate, JobRole
from .forms import CandidateForm, JobRoleForm, CandidateSelfUpdateForm, CandidateStatusForm

logger = logging.getLogger(__name__)


def hr_required(view_func):
    """Decorator: HR Admin only."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_hr_admin:
            messages.error(request, 'Access denied. HR Admin privileges required.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ============================================================
# JOB ROLES
# ============================================================

@method_decorator(hr_required, name='dispatch')
class JobRoleListView(View):
    template_name = 'candidates/job_roles.html'

    def get(self, request):
        roles = JobRole.objects.all().order_by('-created_at')
        query = request.GET.get('q', '')
        if query:
            roles = roles.filter(Q(title__icontains=query) | Q(department__icontains=query))
        paginator = Paginator(roles, 10)
        page = paginator.get_page(request.GET.get('page'))
        form = JobRoleForm()
        return render(request, self.template_name, {'roles': page, 'form': form, 'query': query})

    def post(self, request):
        form = JobRoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.created_by = request.user
            role.save()
            messages.success(request, f'Job role "{role.title}" created successfully!')
            return redirect('candidates:job_roles')
        roles = JobRole.objects.all().order_by('-created_at')
        paginator = Paginator(roles, 10)
        page = paginator.get_page(request.GET.get('page'))
        return render(request, self.template_name, {'roles': page, 'form': form})


@method_decorator(hr_required, name='dispatch')
class JobRoleEditView(View):
    template_name = 'candidates/job_role_edit.html'

    def get(self, request, pk):
        role = get_object_or_404(JobRole, pk=pk)
        form = JobRoleForm(instance=role)
        return render(request, self.template_name, {'form': form, 'role': role})

    def post(self, request, pk):
        role = get_object_or_404(JobRole, pk=pk)
        form = JobRoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job role updated successfully!')
            return redirect('candidates:job_roles')
        return render(request, self.template_name, {'form': form, 'role': role})


@method_decorator(hr_required, name='dispatch')
class JobRoleDeleteView(View):
    def post(self, request, pk):
        role = get_object_or_404(JobRole, pk=pk)
        title = role.title
        role.delete()
        messages.success(request, f'Job role "{title}" deleted.')
        return redirect('candidates:job_roles')


# ============================================================
# CANDIDATES
# ============================================================

@method_decorator(login_required, name='dispatch')
class CandidateListView(View):
    template_name = 'candidates/candidate_list.html'

    def get(self, request):
        # Candidates see only their own profile
        if request.user.is_candidate:
            try:
                candidate = request.user.candidate_profile
                return redirect('candidates:detail', pk=candidate.pk)
            except:
                return redirect('candidates:apply')

        candidates = Candidate.objects.select_related('applied_role', 'user').all()

        # Filters
        q = request.GET.get('q', '')
        status = request.GET.get('status', '')
        role = request.GET.get('role', '')

        if q:
            candidates = candidates.filter(
                Q(full_name__icontains=q) | Q(email__icontains=q) |
                Q(skills__icontains=q) | Q(current_company__icontains=q)
            )
        if status:
            candidates = candidates.filter(status=status)
        if role:
            candidates = candidates.filter(applied_role__id=role)

        paginator = Paginator(candidates, 12)
        page = paginator.get_page(request.GET.get('page'))
        job_roles = JobRole.objects.filter(is_active=True)

        return render(request, self.template_name, {
            'candidates': page,
            'job_roles': job_roles,
            'status_choices': Candidate.STATUS_CHOICES,
            'filters': {'q': q, 'status': status, 'role': role},
        })


@method_decorator(hr_required, name='dispatch')
class CandidateCreateView(View):
    template_name = 'candidates/candidate_form.html'

    def get(self, request):
        form = CandidateForm()
        return render(request, self.template_name, {'form': form, 'action': 'Add'})

    def post(self, request):
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            # Compute AI score
            candidate.ai_resume_score = candidate.compute_ai_score()
            candidate.save()
            messages.success(request, f'Candidate {candidate.full_name} added. AI Score: {candidate.ai_resume_score}%')
            return redirect('candidates:list')
        return render(request, self.template_name, {'form': form, 'action': 'Add'})


@method_decorator(login_required, name='dispatch')
class CandidateDetailView(View):
    template_name = 'candidates/candidate_detail.html'

    def get(self, request, pk):
        candidate = get_object_or_404(Candidate, pk=pk)
        # Candidates can only see their own
        if request.user.is_candidate:
            try:
                if request.user.candidate_profile.pk != pk:
                    messages.error(request, 'Access denied.')
                    return redirect('dashboard:home')
            except:
                pass
        interviews = candidate.interviews.select_related('interviewer').order_by('-scheduled_at')
        status_form = CandidateStatusForm(instance=candidate)
        return render(request, self.template_name, {
            'candidate': candidate,
            'interviews': interviews,
            'status_form': status_form,
        })


@method_decorator(hr_required, name='dispatch')
class CandidateUpdateView(View):
    template_name = 'candidates/candidate_form.html'

    def get(self, request, pk):
        candidate = get_object_or_404(Candidate, pk=pk)
        form = CandidateForm(instance=candidate)
        return render(request, self.template_name, {'form': form, 'candidate': candidate, 'action': 'Edit'})

    def post(self, request, pk):
        candidate = get_object_or_404(Candidate, pk=pk)
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            c = form.save(commit=False)
            c.ai_resume_score = c.compute_ai_score()
            c.save()
            messages.success(request, 'Candidate updated and AI score recalculated!')
            return redirect('candidates:detail', pk=pk)
        return render(request, self.template_name, {'form': form, 'candidate': candidate, 'action': 'Edit'})


@method_decorator(hr_required, name='dispatch')
class CandidateStatusUpdateView(View):
    def post(self, request, pk):
        candidate = get_object_or_404(Candidate, pk=pk)
        form = CandidateStatusForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, f'Status updated to {candidate.get_status_display()}')
        return redirect('candidates:detail', pk=pk)


@method_decorator(hr_required, name='dispatch')
class CandidateDeleteView(View):
    def post(self, request, pk):
        candidate = get_object_or_404(Candidate, pk=pk)
        name = candidate.full_name
        candidate.delete()
        messages.success(request, f'Candidate {name} removed.')
        return redirect('candidates:list')


@method_decorator(hr_required, name='dispatch')
class ComputeAIScoreView(View):
    """AJAX view to recompute AI resume score."""
    def post(self, request, pk):
        candidate = get_object_or_404(Candidate, pk=pk)
        score = candidate.compute_ai_score()
        candidate.ai_resume_score = score
        candidate.save()
        return JsonResponse({'score': float(score), 'message': f'AI Score updated: {score}%'})


@method_decorator(login_required, name='dispatch')
class CandidateApplyView(View):
    """Candidate self-apply view."""
    template_name = 'candidates/apply.html'

    def get(self, request):
        if not request.user.is_candidate:
            return redirect('candidates:list')
        try:
            candidate = request.user.candidate_profile
            form = CandidateSelfUpdateForm(instance=candidate)
            return render(request, self.template_name, {'form': form, 'candidate': candidate})
        except:
            pass
        form = CandidateSelfUpdateForm()
        job_roles = JobRole.objects.filter(is_active=True)
        return render(request, self.template_name, {'form': form, 'job_roles': job_roles})

    def post(self, request):
        applied_role_id = request.POST.get('applied_role')
        try:
            candidate = request.user.candidate_profile
            form = CandidateSelfUpdateForm(request.POST, request.FILES, instance=candidate)
        except:
            candidate = None
            form = CandidateSelfUpdateForm(request.POST, request.FILES)

        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.full_name = request.user.get_full_name() or request.user.email
            c.email = request.user.email
            if applied_role_id:
                try:
                    c.applied_role = JobRole.objects.get(pk=applied_role_id)
                except:
                    pass
            c.ai_resume_score = c.compute_ai_score()
            c.save()
            messages.success(request, 'Application updated!')
            return redirect('dashboard:home')
        job_roles = JobRole.objects.filter(is_active=True)
        return render(request, self.template_name, {'form': form, 'job_roles': job_roles})
