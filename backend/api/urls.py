from django.urls import path
from . import views

urlpatterns = [
    # Health check endpoints
    path('hello/', views.hello_world, name='hello_world'),
    path('health/', views.health_check, name='health_check'),
    
    # Image upload endpoint
    # Image upload endpoint
    path('upload-image/', views.upload_image, name='upload_image'),
    
    # Product recognition endpoint
    path('recognize-product/', views.recognize_product, name='recognize_product'),
    
    # Cross-platform Price Comparison endpoint
    # Cross-platform Price Comparison endpoint
    path('price-comparison/<str:image_id>/', views.price_comparison, name='price_comparison'),
    
    # Generic Endpoints
    path('compare-prices/', views.ComparePricesAPIView.as_view(), name='compare_prices'),
    path('price-history/', views.PriceHistoryAPIView.as_view(), name='price_history'),
]
