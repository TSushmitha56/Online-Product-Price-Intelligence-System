from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.throttling import AnonRateThrottle
from security.rate_limiters import LoginRateThrottle
from . import views


class ThrottledTokenObtainPairView(TokenObtainPairView):
    """JWT login view with login-specific rate limit (5/min per IP)."""
    throttle_classes = [LoginRateThrottle]


urlpatterns = [
    # Registration
    path('register/', views.register, name='auth_register'),

    # JWT Login / Refresh — login is throttled at 5/min
    path('login/', ThrottledTokenObtainPairView.as_view(), name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),

    # Profile management
    path('profile/', views.profile, name='auth_profile'),
    path('change-password/', views.change_password, name='auth_change_password'),

    # Password reset
    path('forgot-password/', views.forgot_password, name='auth_forgot_password'),
    path('reset-password/', views.reset_password, name='auth_reset_password'),

    # GDPR Compliance
    path('data-export/', views.export_data, name='auth_data_export'),
    path('delete-account/', views.delete_account, name='auth_delete_account'),
]
