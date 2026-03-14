"""
Utility functions for file handling and validation.
"""

import os
import uuid
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from security.validators import sanitize_filename as _sanitize_filename


class ImageValidator:
    """
    Validates uploaded image files.
    
    Checks:
        - File type is allowed (JPEG, PNG, WebP)
        - File size doesn't exceed limit (10MB)
    """
    
    @staticmethod
    def validate_file_type(file):
        """
        Validate that the uploaded file is a supported image format.
        
        Args:
            file: The uploaded file object
            
        Returns:
            str: The MIME type of the file
            
        Raises:
            ValidationError: If the file type is not supported
        """
        # Get the MIME type from the file
        mime_type = file.content_type
        
        if mime_type not in settings.ALLOWED_IMAGE_TYPES:
            raise ValidationError(
                f"Invalid file type: {mime_type}. "
                f"Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
            )
        
        return mime_type
    
    @staticmethod
    def validate_file_size(file):
        """
        Validate that the file size doesn't exceed the maximum limit.
        
        Args:
            file: The uploaded file object
            
        Raises:
            ValidationError: If the file size exceeds the limit
        """
        max_size = settings.MAX_UPLOAD_SIZE
        file_size = file.size
        
        if file_size > max_size:
            max_size_mb = max_size / (1024 * 1024)
            file_size_mb = file_size / (1024 * 1024)
            raise ValidationError(
                f"File size ({file_size_mb:.2f}MB) exceeds maximum limit "
                f"({max_size_mb:.0f}MB)"
            )
        
        return file_size
    
    @staticmethod
    def validate_uploaded_file(file):
        """
        Perform complete validation on the uploaded file.
        
        Args:
            file: The uploaded file object
            
        Returns:
            dict: Contains 'mime_type' and 'file_size'
            
        Raises:
            ValidationError: If any validation fails
        """
        if not file:
            raise ValidationError("No file provided")
        
        mime_type = ImageValidator.validate_file_type(file)
        file_size = ImageValidator.validate_file_size(file)
        
        return {
            'mime_type': mime_type,
            'file_size': file_size
        }


class ImageStorage:
    """
    Handles image storage and file naming.
    """
    
    @staticmethod
    def generate_image_id():
        """
        Generate a unique image identifier.
        
        Uses UUID with timestamp prefix for better readability.
        
        Returns:
            str: Unique image identifier (e.g., '20260217_550e8400e29b41d4a716446655440000')
        """
        timestamp = datetime.now().strftime('%Y%m%d')
        unique_id = str(uuid.uuid4()).replace('-', '')
        return f"{timestamp}_{unique_id}"
    
    @staticmethod
    def generate_stored_filename(original_filename, image_id):
        """
        Generate a unique filename for storage.
        
        Args:
            original_filename: The original filename from upload
            image_id: The unique image identifier
            
        Returns:
            str: Filename for storage (e.g., '550e8400e29b41d4a716446655440000.jpg')
        """
        # Get file extension from original filename
        _, ext = os.path.splitext(original_filename)
        
        # Use image_id as base filename with original extension
        stored_filename = f"{image_id}{ext.lower()}"
        
        return stored_filename
    
    @staticmethod
    def ensure_upload_directory_exists():
        """
        Ensure the upload and preprocessed directories exist.
        
        Creates the directories if they don't exist.
        """
        upload_dir = settings.MEDIA_ROOT / 'images'
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        preprocessed_dir = settings.MEDIA_ROOT / 'preprocessed'
        preprocessed_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_processed_filepath(stored_filename):
        """
        Generate the absolute path for the preprocessed image.
        """
        return settings.MEDIA_ROOT / 'preprocessed' / stored_filename
