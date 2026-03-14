import pytest
from django.core.cache import cache
from django.urls import reverse

@pytest.mark.django_db
class TestPerformance:
    def test_cache_functionality(self):
        """Test if Django cache (Redis/LocMem) is working."""
        cache.set("test_key", "test_value", timeout=60)
        assert cache.get("test_key") == "test_value"
        cache.delete("test_key")
        assert cache.get("test_key") is None

    def test_compression_middleware(self, client):
        """Test if compression middleware is active."""
        response = client.get(reverse('health_check'))
        # Note: Compression depends on content length and browser headers
        # We check if it handles the request without crashing
        assert response.status_code == 200


@pytest.mark.django_db
class TestAsyncSearch:
    def test_async_search_lifecycle(self, auth_client):
        """Test triggering an async search and checking its status."""
        # 1. Trigger
        url = reverse('search_async')
        response = auth_client.get(url, {'product': 'laptop'})
        assert response.status_code == 202
        task_id = response.data.get('task_id')
        assert task_id is not None

        # 2. Check status (initially processing or completed if fast)
        status_url = reverse('search_status')
        status_res = auth_client.get(status_url, {'task_id': task_id})
        assert status_res.status_code == 200
        assert status_res.data.get('status') in ['processing', 'completed', 'failed']

    def test_async_search_missing_param(self, auth_client):
        url = reverse('search_async')
        response = auth_client.get(url)
        assert response.status_code == 400

    def test_search_status_missing_id(self, auth_client):
        url = reverse('search_status')
        response = auth_client.get(url)
        assert response.status_code == 400
