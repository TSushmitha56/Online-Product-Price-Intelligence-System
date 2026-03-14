"""
Custom DRF throttle (rate limiter) classes.

Each class applies a distinct limit to a specific endpoint category,
giving fine-grained control over abuse prevention.

Rates are read from settings where possible so they can be tuned via env vars.
"""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, SimpleRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """
    Strict rate limit on login / registration attempts.

    Limit: 5 requests per minute per IP address.
    Applies to: /api/auth/login/, /api/auth/register/

    Prevents brute-force password attacks and credential stuffing.
    """
    scope = 'login'
    rate = '5/min'


class UploadRateThrottle(UserRateThrottle):
    """
    Rate limit on image upload requests.

    Limit: 10 requests per minute per authenticated user.
    Applies to: /api/upload/

    Prevents excessive storage consumption and server load from bulk uploads.
    """
    scope = 'upload'
    rate = '10/min'


class RecognitionRateThrottle(UserRateThrottle):
    """
    Rate limit on product recognition (ML inference) requests.

    Limit: 10 requests per minute per authenticated user.
    Applies to: /api/recognize/

    Prevents abuse of the ML model which is resource-intensive.
    """
    scope = 'recognition'
    rate = '10/min'


class ScrapingRateThrottle(UserRateThrottle):
    """
    Rate limit on price comparison / web scraping requests.

    Limit: 15 requests per minute per authenticated user.
    Applies to: /api/compare/, /api/compare-prices/

    Prevents excessive scraping that could trigger bans on third-party sites
    and place undue load on the backend scrapers.
    """
    scope = 'scraping'
    rate = '15/min'


class ForgotPasswordRateThrottle(AnonRateThrottle):
    """
    Rate limit on password-reset email requests.

    Limit: 3 requests per minute per IP.
    Applies to: /api/auth/forgot-password/

    Prevents email flooding / abuse of the password reset flow.
    """
    scope = 'forgot_password'
    rate = '3/min'
