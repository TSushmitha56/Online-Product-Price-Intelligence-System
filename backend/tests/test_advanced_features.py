import pytest
from django.urls import reverse
from advanced.models import PriceAlert, Wishlist, SearchHistory

@pytest.mark.django_db
class TestAdvancedFeatures:
    def test_price_alerts_pagination(self, auth_client, test_user):
        """Test pagination for price alerts."""
        # Create 15 alerts
        for i in range(15):
            PriceAlert.objects.create(
                user=test_user,
                product_name=f'Product {i}',
                target_price=100.00
            )

        url = reverse('alerts_list_create')
        response = auth_client.get(url)
        assert response.status_code == 200
        # DRF pagination returns 'count', 'next', 'previous', 'results'
        assert 'results' in response.data
        assert len(response.data['results']) == 10
        assert response.data['count'] == 15
        assert response.data['next'] is not None

    def test_wishlist_pagination(self, auth_client, test_user):
        """Test pagination for wishlist."""
        for i in range(15):
            Wishlist.objects.create(
                user=test_user,
                product_name=f'Wish {i}',
                product_url=f'https://example.com/{i}'
            )

        url = reverse('wishlist_list_create')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 10
        assert response.data['count'] == 15

    def test_search_history_pagination(self, auth_client, test_user):
        """Test pagination for search history."""
        for i in range(15):
            SearchHistory.objects.create(
                user=test_user,
                query=f'Search {i}'
            )

        url = reverse('search_history')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 10
        assert response.data['count'] == 15
