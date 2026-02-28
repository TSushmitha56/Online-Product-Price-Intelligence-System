from django.db import models
from django.utils import timezone
import uuid


class Image(models.Model):
    """
    Image model to store information about uploaded images.
    
    Fields:
        - id: UUID primary key for unique identification
        - image_id: String identifier for API responses
        - original_filename: Original name of the uploaded file
        - stored_filename: Name of the file stored on disk
        - file: The actual image file
        - file_size: Size of the file in bytes
        - mime_type: MIME type of the image
        - uploaded_at: Timestamp when the image was uploaded
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_id = models.CharField(max_length=255, unique=True, db_index=True)
    original_filename = models.CharField(max_length=255)
    stored_filename = models.CharField(max_length=255)
    processed_path = models.CharField(max_length=255, null=True, blank=True)
    file = models.ImageField(upload_to='images/%Y/%m/%d/')
    file_size = models.BigIntegerField()  # Size in bytes
    mime_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
    
    def __str__(self):
        return f"{self.image_id} - {self.original_filename}"
    
    def get_file_size_mb(self):
        """Convert file size to MB"""
        return round(self.file_size / (1024 * 1024), 2)
