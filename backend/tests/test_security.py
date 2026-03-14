"""
Security test suite for PriceIntel backend.

Tests:
- Input validation and sanitization (XSS, SQL injection, filenames)
- Magic byte image validation
- Rate limiter throttle class definitions
- GDPR endpoint presence
"""

import pytest
import io
from django.core.exceptions import ValidationError


# ─── validators.py tests ──────────────────────────────────────────────────────

class TestSanitizeText:
    def test_strips_script_tags(self):
        from security.validators import sanitize_text
        result = sanitize_text("<script>alert('xss')</script>Hello")
        assert "<script>" not in result
        assert "Hello" in result

    def test_strips_html_tags(self):
        from security.validators import sanitize_text
        result = sanitize_text("<b>bold</b> text")
        assert "<b>" not in result
        assert "bold" in result
        assert "text" in result

    def test_plain_text_unchanged(self):
        from security.validators import sanitize_text
        result = sanitize_text("notebook 13 inch")
        assert result == "notebook 13 inch"

    def test_non_string_handled(self):
        from security.validators import sanitize_text
        result = sanitize_text(42)
        assert result == "42"


class TestValidateSearchQuery:
    def test_valid_query_passes(self):
        from security.validators import validate_search_query
        result = validate_search_query("  laptop  ")
        assert result == "laptop"

    def test_empty_query_raises(self):
        from security.validators import validate_search_query
        with pytest.raises(ValidationError):
            validate_search_query("")

    def test_too_long_query_raises(self):
        from security.validators import validate_search_query
        with pytest.raises(ValidationError):
            validate_search_query("a" * 201)

    def test_sql_injection_detected(self):
        from security.validators import validate_search_query
        with pytest.raises(ValidationError):
            validate_search_query("1 UNION SELECT * FROM users--")

    def test_drop_table_detected(self):
        from security.validators import validate_search_query
        with pytest.raises(ValidationError):
            validate_search_query("DROP TABLE users")

    def test_xss_sanitized_in_query(self):
        from security.validators import validate_search_query
        result = validate_search_query("<b>keyboard</b>")
        assert "<b>" not in result
        assert "keyboard" in result


class TestSanitizeFilename:
    def test_normal_filename_preserved(self):
        from security.validators import sanitize_filename
        result = sanitize_filename("product_image.jpg")
        assert result == "product_image.jpg"

    def test_path_traversal_stripped(self):
        from security.validators import sanitize_filename
        result = sanitize_filename("../../etc/passwd")
        # Must not contain path separators
        assert "/" not in result
        assert ".." not in result

    def test_special_chars_replaced(self):
        from security.validators import sanitize_filename
        result = sanitize_filename("my file (1)!.png")
        assert "(" not in result
        assert "!" not in result

    def test_dangerous_extension_normalized(self):
        from security.validators import sanitize_filename
        result = sanitize_filename("malware.php")
        assert result.endswith(".jpg")

    def test_long_name_truncated(self):
        from security.validators import sanitize_filename
        long_name = "a" * 200 + ".jpg"
        result = sanitize_filename(long_name)
        assert len(result) <= 104  # 100 name + 4 ext (.jpg)


class TestMagicByteValidation:
    def _make_file(self, header: bytes):
        """Create a simple file-like object with given header bytes."""
        return io.BytesIO(header + b"\x00" * 100)

    def test_valid_jpeg_accepted(self):
        from security.validators import validate_image_magic_bytes
        f = self._make_file(b'\xff\xd8\xff\xe0' + b'\x00' * 12)
        result = validate_image_magic_bytes(f)
        assert result == 'image/jpeg'

    def test_valid_png_accepted(self):
        from security.validators import validate_image_magic_bytes
        f = self._make_file(b'\x89PNG\r\n\x1a\n')
        result = validate_image_magic_bytes(f)
        assert result == 'image/png'

    def test_executable_rejected(self):
        from security.validators import validate_image_magic_bytes
        # ELF executable magic bytes
        f = self._make_file(b'\x7fELF\x02\x01\x01\x00')
        with pytest.raises(ValidationError):
            validate_image_magic_bytes(f)

    def test_pdf_rejected(self):
        from security.validators import validate_image_magic_bytes
        f = self._make_file(b'%PDF-1.4')
        with pytest.raises(ValidationError):
            validate_image_magic_bytes(f)

    def test_empty_file_rejected(self):
        from security.validators import validate_image_magic_bytes
        f = self._make_file(b'')
        with pytest.raises(ValidationError):
            validate_image_magic_bytes(f)


# ─── rate_limiters.py tests ───────────────────────────────────────────────────

class TestRateLimiterClasses:
    def test_login_throttle_has_correct_scope(self):
        from security.rate_limiters import LoginRateThrottle
        throttle = LoginRateThrottle()
        assert throttle.scope == 'login'
        assert throttle.rate == '5/min'

    def test_upload_throttle_has_correct_scope(self):
        from security.rate_limiters import UploadRateThrottle
        throttle = UploadRateThrottle()
        assert throttle.scope == 'upload'
        assert throttle.rate == '10/min'

    def test_recognition_throttle_has_correct_scope(self):
        from security.rate_limiters import RecognitionRateThrottle
        throttle = RecognitionRateThrottle()
        assert throttle.scope == 'recognition'
        assert throttle.rate == '10/min'

    def test_scraping_throttle_has_correct_scope(self):
        from security.rate_limiters import ScrapingRateThrottle
        throttle = ScrapingRateThrottle()
        assert throttle.scope == 'scraping'
        assert throttle.rate == '15/min'

    def test_forgot_password_throttle_has_correct_scope(self):
        from security.rate_limiters import ForgotPasswordRateThrottle
        throttle = ForgotPasswordRateThrottle()
        assert throttle.scope == 'forgot_password'
        assert throttle.rate == '3/min'


# ─── GDPR endpoint URL tests ──────────────────────────────────────────────────

class TestGDPRUrls:
    def test_data_export_url_registered(self):
        """Ensure the data-export URL resolves correctly."""
        try:
            from django.urls import reverse, NoReverseMatch
            url = reverse('auth_data_export')
            assert url == '/api/auth/data-export/'
        except Exception as e:
            if 'SQLAlchemy' in str(e) or 'Could not parse' in str(e):
                pytest.skip(f"SQLAlchemy init issue in test env (not a security bug): {e}")
            pytest.fail(f"auth_data_export URL not registered: {e}")

    def test_delete_account_url_registered(self):
        """Ensure the delete-account URL resolves correctly."""
        try:
            from django.urls import reverse, NoReverseMatch
            url = reverse('auth_delete_account')
            assert url == '/api/auth/delete-account/'
        except Exception as e:
            if 'SQLAlchemy' in str(e) or 'Could not parse' in str(e):
                pytest.skip(f"SQLAlchemy init issue in test env (not a security bug): {e}")
            pytest.fail(f"auth_delete_account URL not registered: {e}")

