"""
Input sanitization helper for the React frontend.

Usage:
    import { sanitizeInput, validateFileUpload } from '../utils/sanitize';
"""

/**
 * Strip HTML/script tags from a user-typed string before it is sent to the API.
 * This is a defence-in-depth measure; the backend also sanitizes all inputs.
 *
 * @param {string} value - Raw user input
 * @returns {string} - Cleaned string
 */
export function sanitizeInput(value) {
  if (typeof value !== 'string') return String(value ?? '');
  return value
    .replace(/<script[\s\S]*?>[\s\S]*?<\/script>/gi, '')
    .replace(/<[^>]+>/g, '')       // strip remaining HTML tags
    .replace(/javascript:/gi, '')   // strip javascript: URIs
    .replace(/on\w+\s*=/gi, '')     // strip inline event handlers
    .trim();
}

/**
 * Client-side file upload validation.
 * The backend performs a stricter server-side check; this gives instant feedback.
 *
 * @param {File} file - The File object from an <input type="file">
 * @param {Object} options
 * @param {number} [options.maxSizeMB=10] - Maximum allowed size in megabytes
 * @param {string[]} [options.allowedTypes] - Allowed MIME types
 * @returns {{ valid: boolean, error: string|null }}
 */
export function validateFileUpload(file, options = {}) {
  const {
    maxSizeMB = 10,
    allowedTypes = ['image/jpeg', 'image/png', 'image/webp'],
  } = options;

  if (!file) {
    return { valid: false, error: 'No file selected.' };
  }

  if (!allowedTypes.includes(file.type)) {
    return {
      valid: false,
      error: `Invalid file type: ${file.type}. Please upload a JPEG, PNG, or WebP image.`,
    };
  }

  const maxSizeBytes = maxSizeMB * 1024 * 1024;
  if (file.size > maxSizeBytes) {
    return {
      valid: false,
      error: `File is too large (${(file.size / 1024 / 1024).toFixed(1)} MB). Maximum allowed size is ${maxSizeMB} MB.`,
    };
  }

  return { valid: true, error: null };
}

/**
 * Sanitize a search query string before submission.
 *
 * @param {string} query
 * @returns {{ valid: boolean, value: string, error: string|null }}
 */
export function validateSearchQuery(query) {
  const cleaned = sanitizeInput(query);

  if (!cleaned || cleaned.length === 0) {
    return { valid: false, value: '', error: 'Search query cannot be empty.' };
  }

  if (cleaned.length > 200) {
    return { valid: false, value: cleaned, error: 'Search query must be 200 characters or fewer.' };
  }

  return { valid: true, value: cleaned, error: null };
}
