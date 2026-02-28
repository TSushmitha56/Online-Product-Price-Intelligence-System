"""
API Views for the backend application.

Includes endpoints for:
    - Hello World (test endpoint)
    - Health Check (system status)
    - Image Upload (core functionality)
"""

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Image
from .utils import ImageValidator, ImageStorage
from image_preprocessing import preprocess_image
import os
from recognition.predictor import predict_product_from_path


@api_view(['GET'])
def hello_world(request):
    """
    Hello World API endpoint.
    
    Used for testing basic connectivity.
    
    Returns:
        Response: Simple greeting message
    """
    return Response({
        "message": "Hello World from Django!",
        "status": "success"
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint.
    
    Used to verify the backend service is running.
    
    Returns:
        Response: Service health status
    """
    return Response({
        "status": "healthy",
        "service": "backend-api"
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def upload_image(request):
    """
    Image upload endpoint.
    
    Accepts image files (JPEG, PNG, WebP) and stores them with validation.
    
    Request:
        - Method: POST
        - Form Data: 'file' (multipart/form-data)
    
    File Requirements:
        - Type: JPEG, PNG, or WebP
        - Maximum size: 10MB
    
    Returns:
        Success (200):
            {
                "status": "success",
                "image_id": "<unique_id>",
                "filename": "<stored_filename>",
                "original_filename": "<original_name>",
                "file_size": <bytes>,
                "file_size_mb": <float>,
                "timestamp": "<upload_time>"
            }
        
        Error (400/413):
            {
                "status": "error",
                "message": "<error_description>"
            }
    """
    try:
        # Check if file is provided
        if 'file' not in request.FILES:
            return Response(
                {
                    "status": "error",
                    "message": "No file provided. Please upload an image file."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        # Validate the uploaded file
        try:
            validation_result = ImageValidator.validate_uploaded_file(uploaded_file)
        except ValidationError as e:
            return Response(
                {
                    "status": "error",
                    "message": str(e.message) if hasattr(e, 'message') else str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ensure upload directory exists
        ImageStorage.ensure_upload_directory_exists()
        
        # Generate unique identifiers
        image_id = ImageStorage.generate_image_id()
        stored_filename = ImageStorage.generate_stored_filename(
            uploaded_file.name,
            image_id
        )
        
        # Create and save the Image model instance
        image_instance = Image.objects.create(
            image_id=image_id,
            original_filename=uploaded_file.name,
            stored_filename=stored_filename,
            file=uploaded_file,
            file_size=uploaded_file.size,
            mime_type=validation_result['mime_type']
        )
        
        # Process the image
        processed_filepath = ImageStorage.get_processed_filepath(stored_filename)
        processed_relative_path = f"preprocessed/{stored_filename}"
        processed_url = f"/media/{processed_relative_path}"
        
        try:
            preprocess_image(
                image_path=image_instance.file.path,
                output_path=processed_filepath
            )
            image_instance.processed_path = processed_relative_path
            image_instance.save(update_fields=['processed_path'])
        except Exception as e:
            print(f"Error during image preprocessing: {e}")
            processed_url = None
        
        # Return success response
        return Response(
            {
                "status": "success",
                "message": "Image uploaded successfully",
                "image_id": image_instance.image_id,
                "original_path": image_instance.file.url,
                "processed_path": processed_url,
                "filename": image_instance.stored_filename,
                "original_filename": image_instance.original_filename,
                "file_size": image_instance.file_size,
                "file_size_mb": round(image_instance.file_size / (1024 * 1024), 2),
                "mime_type": image_instance.mime_type,
                "timestamp": image_instance.uploaded_at.isoformat()
            },
            status=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Unexpected error during image upload: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return Response(
            {
                "status": "error",
                "message": f"An unexpected error occurred during upload. Please try again. Error: {str(e)}"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def recognize_product(request):
    """
    Product image recognition endpoint.
    
    Accepts an image_id and triggers the CNN model on the preprocessed image.
    
    Request:
        - Method: POST
        - JSON:
            {
                "image_id": "<uuid>"
            }
            
    Returns:
        JSON with product category, keywords, and confidences.
    """
    
    image_id = request.data.get('image_id')
    
    if not image_id:
        return Response(
            {"status": "error", "message": "No image_id provided"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    try:
        image_instance = Image.objects.get(image_id=image_id)
    except Image.DoesNotExist:
        return Response(
            {"status": "error", "message": "Image not found"},
            status=status.HTTP_404_NOT_FOUND
        )
        
    if not image_instance.processed_path:
        return Response(
            {"status": "error", "message": "Image has no preprocessed path available."},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    try:
        # Resolve absolute path to the processed image
        abs_path = str(settings.MEDIA_ROOT / image_instance.processed_path)
        
        # Run recognition
        prediction_result = predict_product_from_path(abs_path)
        
        return Response(
            {
                "status": "success",
                "image_id": image_instance.image_id,
                "recognition": prediction_result
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        print(f"Error during image recognition: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return Response(
            {
                "status": "error",
                "message": "An error occurred during recognition."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
