"""api/urls.py - DRF Router"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'job-roles', views.JobRoleViewSet, basename='jobrole')
router.register(r'candidates', views.CandidateViewSet, basename='candidate')
router.register(r'interviews', views.InterviewViewSet, basename='interview')
router.register(r'feedback', views.FeedbackViewSet, basename='feedback')
router.register(r'stats', views.DashboardStatsViewSet, basename='stats')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('rest_framework.urls')),
]
