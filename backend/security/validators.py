"""
Input validation and sanitization utilities.

Protects against:
- Cross-Site Scripting (XSS)
- Path traversal attacks
- Malicious file uploads (magic byte validation)
- Oversized or invalid search queries
"""

import re
import os
import struct
import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Text Sanitization
# ---------------------------------------------------------------------------

def sanitize_text(value: str) -> str:
    """
    Strip HTML and script tags from user-provided text.

    Uses a simple regex approach when bleach is unavailable,
    or bleach when installed (added in requirements.txt).
    """
    if not isinstance(value, str):
        return str(value)
    try:
        import bleach
        return bleach.clean(value, tags=[], attributes={}, strip=True)
    except ImportError:
        # Fallback: strip tags manually
        clean = re.sub(r'<[^>]+>', '', value)
        return clean.strip()


def validate_search_query(query: str) -> str:
    """
    Validate and sanitize a product search query.

    Rules:
    - Must be a string between 1 and 200 characters after strip
    - Must not contain SQL injection patterns
    - Sanitized for XSS

    Returns the cleaned query.
    Raises ValidationError with a user-friendly message on failure.
    """
    if not query or not isinstance(query, str):
        raise ValidationError("Search query must be a non-empty string.")

    query = query.strip()

    if len(query) < 1:
        raise ValidationError("Search query cannot be empty.")
    if len(query) > 200:
        raise ValidationError("Search query must not exceed 200 characters.")

    # Detect obvious SQL injection patterns
    sql_patterns = [
        r"(\bUNION\b.*\bSELECT\b)",
        r"(\bDROP\b.*\bTABLE\b)",
        r"(\bINSERT\b.*\bINTO\b)",
        r"--\s",
        r";\s*--",
        r"/\*.*\*/",
    ]
    query_upper = query.upper()
    for pattern in sql_patterns:
        if re.search(pattern, query_upper):
            logger.warning(f"Potential SQL injection attempt in query: {query[:50]!r}")
            raise ValidationError("Invalid characters detected in search query.")

    # Sanitize XSS
    return sanitize_text(query)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize an uploaded file's original name.

    - Strip directory separators (path traversal prevention)
    - Remove characters outside the safe set
    - Enforce that only the base name is kept
    - Limit to 100 characters (before extension)
    """
    if not filename:
        return "upload"

    # Take only the base name — prevent path traversal like ../../etc/passwd
    filename = os.path.basename(filename)

    # Split into name + extension
    name, ext = os.path.splitext(filename)

    # Allow only alphanumerics, hyphens, underscores, spaces
    name = re.sub(r'[^a-zA-Z0-9_\-\s]', '_', name)
    name = re.sub(r'\s+', '_', name)
    name = name[:100]

    # Force lowercase, known-safe extension
    ext = ext.lower()
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    if ext not in allowed_extensions:
        ext = '.jpg'  # fallback — actual type check is done by magic bytes

    return f"{name}{ext}" if name else f"upload{ext}"


# ---------------------------------------------------------------------------
# Magic Byte Validation
# ---------------------------------------------------------------------------

# Magic byte signatures for allowed image types
_IMAGE_SIGNATURES = {
    'image/jpeg': [(0, b'\xff\xd8\xff')],
    'image/png':  [(0, b'\x89PNG\r\n\x1a\n')],
    'image/webp': [(0, b'RIFF'), (8, b'WEBP')],
}


def validate_image_magic_bytes(file) -> str:
    """
    Verify a file's true type by inspecting its magic bytes.

    This prevents attackers from renaming an executable as image.jpg.

    Args:
        file: A Django InMemoryUploadedFile or similar file-like object.

    Returns:
        Detected MIME type string.

    Raises:
        ValidationError: If the file does not match any allowed image signature.
    """
    file.seek(0)
    header = file.read(16)
    file.seek(0)

    for mime_type, signatures in _IMAGE_SIGNATURES.items():
        match = True
        for offset, magic in signatures:
            if len(header) < offset + len(magic):
                match = False
                break
            if header[offset:offset + len(magic)] != magic:
                match = False
                break
        if match:
            return mime_type

    logger.warning("File rejected: magic bytes do not match any allowed image type.")
    raise ValidationError(
        "Uploaded file is not a valid image. Only JPEG, PNG, and WebP are accepted."
    )


# ---------------------------------------------------------------------------
# Request Body Sanitization
# ---------------------------------------------------------------------------

def sanitize_request_data(data: dict, text_fields: list) -> dict:
    """
    Sanitize specified text fields in a request data dictionary.

    Args:
        data: The request.data dictionary.
        text_fields: List of field names to sanitize.

    Returns:
        A new dict with sanitized values.
    """
    sanitized = dict(data)
    for field in text_fields:
        if field in sanitized and isinstance(sanitized[field], str):
            sanitized[field] = sanitize_text(sanitized[field])
    return sanitized
