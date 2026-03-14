from django.urls import path
from . import views

urlpatterns = [
    # Price Alerts
    path('alerts/', views.alerts_list_create, name='alerts_list_create'),
    path('alerts/<int:pk>/', views.alert_detail, name='alert_detail'),

    # Search History
    path('search-history/', views.search_history, name='search_history'),

    # Wishlist
    path('wishlist/', views.wishlist_list_create, name='wishlist_list_create'),
    path('wishlist/<int:pk>/', views.wishlist_delete, name='wishlist_delete'),

    # Price History (for chart)
    path('price-history/', views.price_history, name='adv_price_history'),

    # Recommendations
    path('recommendations/', views.recommendations, name='recommendations'),
]
