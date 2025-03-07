import asyncio
import time

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.cache import LRUCache
from app.config import app_config


client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def mock_cache_instance(monkeypatch: pytest.MonkeyPatch):
    """Подменяем объект CACHE новым экземпляром LRUCache."""
    monkeypatch.setattr(app_config, 'capacity_cache', 2)
    
    test_cache = LRUCache()
    
    monkeypatch.setattr("api.api.CACHE", test_cache)

    return test_cache


@pytest.fixture(scope="function")
def setup_cache(mock_cache_instance: LRUCache):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mock_cache_instance.put("test_key_1", "test_key_1"))
    yield
    mock_cache_instance.cache.clear()


class TestCacheAPI:

    def test_get_existing_key(self, setup_cache: None):
        response = client.get("/cache/test_key_1")

        assert response.status_code == 200
        assert response.json() == "test_key_1"

    def test_get_key_not_found(self, setup_cache: None):
        response = client.get("/cache/any_test_key")

        assert response.status_code == 404
        assert response.json() == {'detail': 'Key not found'}

    def test_add_key_to_cache(self, setup_cache: None, mock_cache_instance: LRUCache):
        response = client.put("/cache/test_key_2", json={"value": "test_value_2"})

        assert response.status_code == 201
        assert len(mock_cache_instance.cache) == 2

    def test_update_value_in_cache(self, setup_cache: None, mock_cache_instance: LRUCache):
        response = client.put("/cache/test_key_1", json={"value": "new_test_value"})

        assert response.status_code == 200
        assert mock_cache_instance.cache.get("test_key_1") == ('new_test_value', None)

    def test_add_key_in_full_cache(self, setup_cache: None, mock_cache_instance: LRUCache):
        response = client.put("/cache/test_key_2", json={"value": "test_value_2"})

        assert list(mock_cache_instance.cache.items()) == [('test_key_2', ('test_value_2', None)), ('test_key_1', ('test_key_1', None))]

        response = client.put("/cache/test_key_3", json={"value": "test_value_3"})

        assert len(mock_cache_instance.cache) == 2
        assert list(mock_cache_instance.cache.items()) == [('test_key_3', ('test_value_3', None)), ('test_key_2', ('test_value_2', None))]
    
    def test_delete_value_in_cache(self, setup_cache: None, mock_cache_instance: LRUCache):
        response = client.delete("/cache/test_key_1")

        assert response.status_code == 204
        assert mock_cache_instance.cache.get("test_key_1") == (None, None)

    def test_delete_valuer_key_not_found(self, setup_cache: None):
        response = client.delete("/cache/test_key_2")

        assert response.status_code == 404
        assert response.json() == {'detail': 'Key not found'}


    def test_get_static_cache(self, setup_cache: None):
        response = client.get("/cache/stats")

        assert response.status_code == 200
        assert response.json() == {'size': 1, 'capacity': 2, 'items': ['test_key_1']}

    def test_put_key_with_ttl(self, setup_cache: None, mock_cache_instance: LRUCache):
        response = client.put("/cache/test_key_2", json={"value": "new_test_value", "ttl": 60})

        assert response.status_code == 201

        value, ttl = mock_cache_instance.cache.get("test_key_2")

        assert value == "new_test_value"
        assert ttl > time.time() + 30
    
    def test_not_validate_ttl_for_put(self, setup_cache: None):
        response = client.put("/cache/test_key_1", json={"value": "new_test_value", "ttl": -1})

        assert response.status_code == 422

    def test_get_key_for_expired_ttl(self, setup_cache: None, mock_cache_instance: LRUCache):
        client.put("/cache/test_key_2", json={"value": "new_test_value", "ttl": 1})

        time.sleep(1)
        response = client.get("/cache/test_key_2")

        assert response.status_code == 404
        assert response.json() == {'detail': 'Key not found'}
        assert len(mock_cache_instance.cache) == 1
