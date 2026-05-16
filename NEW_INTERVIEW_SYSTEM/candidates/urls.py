"""candidates/urls.py"""
from django.urls import path
from . import views

app_name = 'candidates'

urlpatterns = [
    # Job Roles
    path('roles/', views.JobRoleListView.as_view(), name='job_roles'),
    path('roles/<int:pk>/edit/', views.JobRoleEditView.as_view(), name='job_role_edit'),
    path('roles/<int:pk>/delete/', views.JobRoleDeleteView.as_view(), name='job_role_delete'),

    # Candidates
    path('', views.CandidateListView.as_view(), name='list'),
    path('add/', views.CandidateCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CandidateDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.CandidateUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CandidateDeleteView.as_view(), name='delete'),
    path('<int:pk>/status/', views.CandidateStatusUpdateView.as_view(), name='status_update'),
    path('<int:pk>/ai-score/', views.ComputeAIScoreView.as_view(), name='ai_score'),
    path('apply/', views.CandidateApplyView.as_view(), name='apply'),
]
