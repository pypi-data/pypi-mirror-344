"""Tests for the cache store manager."""

from datetime import UTC, datetime

import pytest

from graph_context.caching.cache_store import CacheEntry
from graph_context.caching.cache_store_manager import CacheStoreManager
from graph_context.caching.config import CacheConfig


@pytest.fixture
def config():
    """Create a test cache configuration."""
    return CacheConfig(
        entity_cache_size=10,
        entity_cache_ttl=60.0,
        relation_cache_size=10,
        relation_cache_ttl=60.0,
        query_cache_size=5,
        query_cache_ttl=30.0,
        traversal_cache_size=5,
        traversal_cache_ttl=30.0,
    )


@pytest.fixture
def store_manager(config):
    """Create a test cache store manager."""
    return CacheStoreManager(config)


@pytest.mark.asyncio
async def test_store_initialization(store_manager, config):
    """Test that stores are initialized with correct configuration."""
    # Test entity store
    entity_store = store_manager.get_entity_store()
    assert entity_store._cache.maxsize == config.entity_cache_size
    assert entity_store._cache.ttl == config.entity_cache_ttl

    # Test relation store
    relation_store = store_manager.get_relation_store()
    assert relation_store._cache.maxsize == config.relation_cache_size
    assert relation_store._cache.ttl == config.relation_cache_ttl

    # Test query store
    query_store = store_manager.get_query_store()
    assert query_store._cache.maxsize == config.query_cache_size
    assert query_store._cache.ttl == config.query_cache_ttl

    # Test traversal store
    traversal_store = store_manager.get_traversal_store()
    assert traversal_store._cache.maxsize == config.traversal_cache_size
    assert traversal_store._cache.ttl == config.traversal_cache_ttl


@pytest.mark.asyncio
async def test_store_separation(store_manager):
    """Test that each store is a separate instance."""
    entity_store = store_manager.get_entity_store()
    relation_store = store_manager.get_relation_store()
    query_store = store_manager.get_query_store()
    traversal_store = store_manager.get_traversal_store()

    # Verify all stores are different instances
    stores = [entity_store, relation_store, query_store, traversal_store]
    for i in range(len(stores)):
        for j in range(i + 1, len(stores)):
            assert stores[i] is not stores[j]


@pytest.mark.asyncio
async def test_clear_all(store_manager):
    """Test clearing all cache stores."""
    # Set up test data in each store
    entity_store = store_manager.get_entity_store()
    relation_store = store_manager.get_relation_store()
    query_store = store_manager.get_query_store()
    traversal_store = store_manager.get_traversal_store()

    # Create test entries
    entity_entry = CacheEntry(
        value={"id": "test_entity"},
        created_at=datetime.now(UTC),
        entity_type="test_type",
    )
    relation_entry = CacheEntry(
        value={"id": "test_relation"},
        created_at=datetime.now(UTC),
        relation_type="test_type",
    )
    query_entry = CacheEntry(
        value={"results": []}, created_at=datetime.now(UTC), query_hash="test_hash"
    )
    traversal_entry = CacheEntry(
        value={"results": []},
        created_at=datetime.now(UTC),
        query_hash="test_hash",  # Traversal uses query_hash field
    )

    # Add test data
    await entity_store.set("test_entity", entity_entry)
    await relation_store.set("test_relation", relation_entry)
    await query_store.set("test_query", query_entry)
    await traversal_store.set("test_traversal", traversal_entry)

    # Verify data is stored
    assert await entity_store.get("test_entity") == entity_entry
    assert await relation_store.get("test_relation") == relation_entry
    assert await query_store.get("test_query") == query_entry
    assert await traversal_store.get("test_traversal") == traversal_entry

    # Clear all stores
    await store_manager.clear_all()

    # Verify all stores are cleared
    assert await entity_store.get("test_entity") is None
    assert await relation_store.get("test_relation") is None
    assert await query_store.get("test_query") is None
    assert await traversal_store.get("test_traversal") is None
