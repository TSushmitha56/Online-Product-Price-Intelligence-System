from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET'])
def hello_world(request):
    """Hello World API endpoint"""
    return Response({
        "message": "Hello World from Django!",
        "status": "success"
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        "status": "healthy",
        "service": "backend-api"
    }, status=status.HTTP_200_OK)
