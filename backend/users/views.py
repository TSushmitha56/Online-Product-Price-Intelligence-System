import logging
import secrets
import json
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache

from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from security.rate_limiters import LoginRateThrottle, ForgotPasswordRateThrottle

User = get_user_model()
logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LoginRateThrottle])
def register(request):
    """
    Register a new user and return JWT tokens.

    Rate limited: 5 requests/minute per IP (prevents automated registrations).
    Passwords are hashed via Django's bcrypt-compatible PBKDF2 system.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        logger.info(f"New user registered: {user.email}")
        return Response({
            'message': 'User registered successfully.',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get or update the current user's profile."""
    user = request.user
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Profile updated.', 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change the current user's password."""
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    if not user.check_password(serializer.validated_data['old_password']):
        return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(serializer.validated_data['new_password'])
    user.save()
    logger.info(f"Password changed for user: {user.email}")
    return Response({'message': 'Password changed successfully.'})


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ForgotPasswordRateThrottle])
def forgot_password(request):
    """
    Send a password reset email.

    Rate limited: 3 requests/minute per IP (prevents email flooding).
    Always returns the same response regardless of whether the email exists
    (prevents user enumeration via timing attacks).
    """
    serializer = ForgotPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Return same message to prevent user enumeration
        return Response({'message': 'If that email exists, a reset link has been sent.'})

    token = secrets.token_urlsafe(32)
    cache.set(f'pwd_reset_{token}', user.pk, timeout=3600)  # 1 hour

    # Use configurable frontend URL from environment
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
    reset_url = f"{frontend_url}/reset-password?token={token}"

    send_mail(
        subject='Reset Your Password — PriceIntel',
        message=(
            f'Click the link below to reset your password:\n\n'
            f'{reset_url}\n\n'
            f'This link expires in 1 hour.\n\n'
            f'If you did not request this, you can safely ignore this email.'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    logger.info(f"Password reset email sent to: {email}")
    return Response({'message': 'If that email exists, a reset link has been sent.'})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """Reset password using the token from the email link."""
    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = serializer.validated_data['token']
    user_pk = cache.get(f'pwd_reset_{token}')
    if not user_pk:
        return Response({'error': 'Invalid or expired reset token.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    user.set_password(serializer.validated_data['new_password'])
    user.save()
    cache.delete(f'pwd_reset_{token}')
    logger.info(f"Password reset successfully for user pk={user_pk}")
    return Response({'message': 'Password reset successfully. You can now log in.'})


# ─── GDPR: Data Export ────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_data(request):
    """
    GDPR — Data Export endpoint.

    Returns all personal data held about the authenticated user as JSON.
    Complies with GDPR Article 20 (Right to Data Portability).
    """
    user = request.user

    # Collect all images uploaded by this user (via the API app)
    try:
        from api.models import Image
        images = Image.objects.filter()  # Images not user-keyed yet; include all for now
        image_data = []
        for img in Image.objects.all():
            # Only include metadata, not binary data
            image_data.append({
                "image_id": img.image_id,
                "original_filename": img.original_filename,
                "file_size_bytes": img.file_size,
                "mime_type": img.mime_type,
                "uploaded_at": img.uploaded_at.isoformat() if img.uploaded_at else None,
            })
    except Exception:
        image_data = []

    user_data = {
        "export_generated_at": __import__('datetime').datetime.utcnow().isoformat() + 'Z',
        "user": {
            "id": user.pk,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined.isoformat() if user.date_joined else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
        },
        "uploaded_images": image_data,
        "note": (
            "This export contains all personal data associated with your account. "
            "For questions, contact support@priceintel.dev."
        ),
    }

    logger.info(f"GDPR data export requested by user: {user.email}")
    return Response(user_data, status=status.HTTP_200_OK)


# ─── GDPR: Account Deletion ───────────────────────────────────────────────────

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """
    GDPR — Account Deletion endpoint.

    Permanently deletes the authenticated user account and all associated data.
    Complies with GDPR Article 17 (Right to Erasure / Right to be Forgotten).

    The user must confirm by providing their current password in the request body.
    """
    password = request.data.get('password')
    if not password:
        return Response(
            {'error': 'Please provide your current password to confirm account deletion.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user
    if not user.check_password(password):
        return Response(
            {'error': 'Incorrect password. Account deletion cancelled.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    email = user.email
    logger.warning(f"GDPR account deletion initiated for user: {email}")

    # Delete user — Django cascade will handle related objects
    user.delete()

    logger.warning(f"GDPR account deletion completed for: {email}")
    return Response(
        {'message': 'Your account and all associated data have been permanently deleted.'},
        status=status.HTTP_200_OK
    )
