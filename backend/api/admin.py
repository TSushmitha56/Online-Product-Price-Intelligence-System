from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Admin interface for managing uploaded images.
    
    Display list showing:
        - Image ID (unique identifier)
        - Original filename
        - File size
        - Upload timestamp
    """
    list_display = (
        'image_id',
        'original_filename',
        'file_size',
        'mime_type',
        'uploaded_at'
    )
    list_filter = ('mime_type', 'uploaded_at')
    search_fields = ('image_id', 'original_filename')
    readonly_fields = (
        'id',
        'image_id',
        'uploaded_at',
        'file_size',
        'mime_type'
    )
    ordering = ('-uploaded_at',)
    
    fieldsets = (
        ('Image Information', {
            'fields': ('id', 'image_id', 'original_filename', 'stored_filename')
        }),
        ('File Details', {
            'fields': ('file', 'file_size', 'mime_type')
        }),
        ('Metadata', {
            'fields': ('uploaded_at',)
        }),
    )
