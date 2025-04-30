# tests/unit/test_indexer.py
import os
import sqlite3

import pytest
from fixture_generator import create_test_graph_fixture

from graph_reader.indexers import get_indexer
from graph_reader.indexers.memory_indexer import MemoryIndexer
from graph_reader.indexers.sqlite_indexer import SQLiteIndexer


def test_get_indexer_errors():
    """Test error cases in get_indexer function."""
    # Test None base_dir
    with pytest.raises(TypeError, match="base_dir cannot be None"):
        get_indexer("memory", None)

    # Test empty base_dir
    with pytest.raises(ValueError, match="base_dir cannot be empty"):
        get_indexer("memory", "")

    # Test unknown indexer type
    with pytest.raises(ValueError, match="Unknown indexer type: invalid"):
        get_indexer("invalid", "some_dir")


def test_get_indexer_success(setup_graph_fixture):
    """Test successful indexer creation."""
    # Test memory indexer
    memory_indexer = get_indexer("memory", setup_graph_fixture)
    assert isinstance(memory_indexer, MemoryIndexer)

    # Test SQLite indexer
    sqlite_indexer = get_indexer("sqlite", setup_graph_fixture)
    assert isinstance(sqlite_indexer, SQLiteIndexer)


@pytest.fixture(scope="session")
def setup_graph_fixture(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test_graph")
    create_test_graph_fixture(base_dir=temp_dir)
    return str(temp_dir)


@pytest.fixture(scope="session")
def setup_sqlite_db(setup_graph_fixture):
    """Setup SQLite database with test data."""
    db_path = os.path.join(setup_graph_fixture, "index.db")

    # Remove existing db if any
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS entity_index (
            entity_id INTEGER,
            name TEXT,
            type TEXT,
            community_id TEXT
        )
    """
    )

    test_data = [
        (1, "Alice", "Person", "team_alpha"),
        (2, "Bob", "Person", "team_alpha"),
        (3, "Charlie", "Person", "team_beta"),
    ]

    cursor.executemany(
        "INSERT OR REPLACE INTO entity_index (entity_id, name, type, community_id) VALUES (?, ?, ?, ?)",
        test_data,
    )
    conn.commit()
    conn.close()

    yield setup_graph_fixture

    # Cleanup after all tests
    if os.path.exists(db_path):
        os.remove(db_path)


class BaseIndexerTest:
    """Base test class for all indexer implementations."""

    @pytest.fixture(scope="module")
    def indexer(self, setup_graph_fixture):
        """Should be overridden by subclasses to provide specific indexer instance."""
        raise NotImplementedError

    def test_search_by_property_name(self, indexer):
        """Test searching by name property."""
        results = indexer.search_by_property("name", "Alice")
        assert isinstance(results, list)
        assert 1 in results

        results = indexer.search_by_property("name", "Bobby")
        assert 2 in results

        results = indexer.search_by_property("name", "Charlie")
        assert 3 in results

    def test_search_by_property_type(self, indexer):
        """Test searching by type property."""
        results = indexer.search_by_property("type", "Person")
        assert set(results) == {0, 1, 2, 3}

    def test_search_by_property_community(self, indexer):
        """Test searching by community_id property."""
        results = indexer.search_by_property("community_id", "team_alpha")
        assert set(results) == {1, 2}

        results = indexer.search_by_property("community_id", "team_beta")
        assert set(results) == {3}

    def test_search_by_property_not_found(self, indexer):
        """Test searching for non-existent property value."""
        results = indexer.search_by_property("name", "David")
        assert results == []

        results = indexer.search_by_property("non_existent", "value")
        assert results == []


class TestMemoryIndexer(BaseIndexerTest):
    """Test class for MemoryIndexer implementation."""

    @pytest.fixture(scope="module")
    def indexer(self, setup_graph_fixture):
        return MemoryIndexer(setup_graph_fixture)


class TestSQLiteIndexer(BaseIndexerTest):
    """Test class for SQLiteIndexer implementation."""

    @pytest.fixture(scope="module")
    def indexer(self, setup_sqlite_db):
        return SQLiteIndexer(setup_sqlite_db)

    def test_sqlite_operational_error(self, setup_sqlite_db):
        """Test that SQLiteIndexer handles operational errors gracefully."""
        indexer = SQLiteIndexer(setup_sqlite_db)
        # Try to search with an invalid column name
        results = indexer.search_by_property("invalid_column", "value")
        assert results == []  # Should return empty list on error
