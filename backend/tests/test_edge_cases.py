import pytest
from django.urls import reverse
from unittest.mock import patch

@pytest.mark.django_db
class TestEdgeCases:
    def test_search_async_no_product(self, auth_client):
        """Test search with empty product query."""
        url = reverse('search_async')
        response = auth_client.get(url, {'product': ''})
        assert response.status_code == 400

    @patch('api.views.search_all_platforms')
    def test_search_async_scraping_failure(self, mock_search, auth_client):
        """Test handling of scraping failures."""
        mock_search.side_effect = Exception("Scraper blocked")
        
        # Trigger search
        url = reverse('search_async')
        response = auth_client.get(url, {'product': 'failing-product'})
        assert response.status_code == 202
        task_id = response.data.get('task_id')
        
        # We need to manually call the background function or wait
        # Since we use executor.submit, it's async. 
        # In a real test we'd use a synchronous executor for testing.
        from api.views import SearchAsyncAPIView
        view = SearchAsyncAPIView()
        view.run_search(task_id, 'failing-product')
        
        # Check status
        status_url = reverse('search_status')
        status_res = auth_client.get(status_url, {'task_id': task_id})
        assert status_res.status_code == 200
        assert status_res.data.get('status') == 'failed'
        assert 'Scraper blocked' in status_res.data.get('error')

    def test_invalid_task_id(self, auth_client):
        """Test status check with non-existent task_id."""
        url = reverse('search_status')
        response = auth_client.get(url, {'task_id': 'non-existent-uuid'})
        assert response.status_code == 404
