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
from comparison.aggregator import aggregate_prices
from scrapers import search_all_platforms
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
import logging
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from db.models import Product, Price
from db.connection import SessionLocal
from .pagination import ComparePricesPagination

logger = logging.getLogger(__name__)


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

@api_view(['GET'])
def price_comparison(request, image_id):
    """
    Combines recognition + web scraping + pricing algorithm to yield the final
    price comparison response.
    """
    try:
        image_instance = Image.objects.get(image_id=image_id)
    except Image.DoesNotExist:
        return Response(
            {"status": "error", "message": "Image not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if not image_instance.processed_path:
        return Response(
            {"status": "error", "message": "Image needs preprocessing first"},
            status=status.HTTP_400_BAD_REQUEST
        )

    abs_path = str(settings.MEDIA_ROOT / image_instance.processed_path)

    # 1. Run inference to identify the product query
    try:
        prediction_result = predict_product_from_path(abs_path)
        
        # Build query from keywords or category
        query = prediction_result.get('category', '').replace('_', ' ')
        if prediction_result.get('keywords') and len(prediction_result['keywords']) > 0:
             query = prediction_result['keywords'][0]
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"status": "error", "message": "Failed to recognize product"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 2. Invoke the Web Scrapers
    try:
        raw_results = search_all_platforms(query)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"status": "error", "message": "Scraping engines failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 3. Aggregate and Score
    agg_result = aggregate_prices(query, [raw_results])
    
    # Absolute URL for fallback product image
    default_img = request.build_absolute_uri(image_instance.file.url)

    # If no matches, yield empty success list
    if not agg_result.get("matched_products"):
         return Response({
             "product": {"name": query, "image": default_img},
             "summary": {},
             "offers": []
         }, status=status.HTTP_200_OK)

    # 4. Map the internal aggregator schema to the external API response contract
    matched = agg_result["matched_products"][0]
    best_store = matched.get("best_overall_offer", {}).get("store")
    best_url = matched.get("best_overall_offer", {}).get("product_url")
    
    mapped_offers = []
    for o in matched.get("offers", []):
        # We manually verify if this listing object matches the best_overall_offer node
        is_best = (o.get('platform') == best_store and o.get('product_url') == best_url)
        
        mapped_offers.append({
             "store": o.get('platform', 'Unknown'),
             "price": o.get('price', 0.0),
             "shipping": o.get('shipping_cost', 0.0),
             "final_price": (o.get('price') or 0.0) + (o.get('shipping_cost') or 0.0),
             "availability": o.get('availability', 'Unknown'),
             "seller_rating": o.get('rating'),
             "product_url": o.get('product_url', '#'),
             "image_url": o.get('image_url') or default_img,
             "is_best_deal": is_best
        })
        
    prices_stats = matched.get("price_stats", {})
    response_data = {
         "product": {
             "name": query,
             "image": default_img
         },
         "summary": {
             "lowest_price": prices_stats.get("lowest"),
             "highest_price": prices_stats.get("highest"),
             "average_price": prices_stats.get("average")
         },
         "offers": mapped_offers
    }

    return Response(response_data, status=status.HTTP_200_OK)


class ComparePricesAPIView(APIView):
    """
    API View to get price comparisons for a specific product name.
    Utilizes Redis caching to avoid redundant scraping.
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='product', description='Product name to search for', required=True, type=str),
            OpenApiParameter(name='page', description='Page number', required=False, type=int),
            OpenApiParameter(name='page_size', description='Number of results per page', required=False, type=int),
        ],
        description="Trigger scraping pipeline if no recent cached result exists, and return normalized JSON response.",
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT}
    )
    def get(self, request):
        product_name = request.query_params.get('product')
        if not product_name or not product_name.strip():
            return Response({"error": "product parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        product_name = product_name.strip()
        cache_key = f"price_compare_v2:{product_name}"
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            logger.info("CACHE_HIT")
            results = cached_data
        else:
            logger.info("CACHE_MISS")
            try:
                raw_results = search_all_platforms(product_name)
                agg_result = aggregate_prices(product_name, [raw_results])
            except Exception as e:
                logger.error(f"Scraping/Aggregation failed: {e}")
                return Response({"error": "Scraping engines failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Extract mapped offers
            results = []
            if agg_result.get("matched_products"):
                matched = agg_result["matched_products"][0]
                best_store = matched.get("best_overall_offer", {}).get("store")
                best_url = matched.get("best_overall_offer", {}).get("product_url")
                
                for o in matched.get("offers", []):
                    is_best = (o.get('platform') == best_store and o.get('product_url') == best_url)
                    results.append({
                        "platform": o.get('platform', 'Unknown'),
                        "title": o.get('title', product_name),
                        "price": float(o.get('price', 0.0) or 0.0),
                        "currency": o.get('currency', 'USD'),
                        "product_url": o.get('product_url', '#'),
                        "image_url": o.get('image_url') or "https://via.placeholder.com/300?text=No+Image"
                    })
            
            # Cache for 15 minutes as per requirements
            cache.set(cache_key, results, timeout=60 * 15)

        # Pagination
        paginator = ComparePricesPagination()
        paginator.product_name = product_name
        paginated_results = paginator.paginate_queryset(results, request, view=self)
        
        if paginated_results is not None:
            return paginator.get_paginated_response(paginated_results)
            
        return Response({
            "product_name": product_name,
            "results": results
        })


class PriceHistoryAPIView(APIView):
    """
    API View to get product price history.
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='product_id', description='UUID of the product', required=True, type=str),
        ],
        description="Return chronological price history for a given product ID.",
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT}
    )
    def get(self, request):
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({"error": "product_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            session = SessionLocal()
            product = session.query(Product).filter(Product.product_id == product_id).first()
            if not product:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
                
            prices = session.query(Price).filter(Price.product_id == product_id).order_by(Price.timestamp).all()
            history = [
                {
                    "date": p.timestamp.strftime("%Y-%m-%d"),
                    "platform": p.store_name,
                    "price": float(p.price)
                }
                for p in prices
            ]
        finally:
            session.close()
            
        return Response({
            "product_id": product_id,
            "history": history
        })
