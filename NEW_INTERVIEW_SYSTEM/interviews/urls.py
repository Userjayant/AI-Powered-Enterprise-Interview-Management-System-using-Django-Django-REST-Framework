"""interviews/urls.py"""
from django.urls import path
from . import views

app_name = 'interviews'

urlpatterns = [
    path('', views.InterviewListView.as_view(), name='list'),
    path('schedule/', views.InterviewScheduleView.as_view(), name='schedule'),
    path('<int:pk>/', views.InterviewDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.InterviewUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.InterviewDeleteView.as_view(), name='delete'),
    path('<int:interview_pk>/feedback/', views.FeedbackSubmitView.as_view(), name='feedback_submit'),
    path('feedback/<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback_detail'),
]
