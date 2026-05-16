"""
Main URL Configuration - AI-Powered Interview Management System
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard:home'), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('candidates/', include('candidates.urls', namespace='candidates')),
    path('interviews/', include('interviews.urls', namespace='interviews')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('api/', include('api.urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site headers
admin.site.site_header = "Interview Management System"
admin.site.site_title = "IMS Admin"
admin.site.index_title = "System Administration"
