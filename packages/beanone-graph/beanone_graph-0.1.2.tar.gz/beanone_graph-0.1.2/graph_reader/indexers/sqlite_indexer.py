import glob
import json
import os
import sqlite3

from .base_indexer import BaseIndexer


class SQLiteIndexer(BaseIndexer):
    def __init__(self, base_dir):
        self.db_path = os.path.join(base_dir, "index.db")
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()
        self._build_index_from_entities(base_dir)

    def _create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS entity_index (
                    entity_id INTEGER PRIMARY KEY,
                    name TEXT,
                    type TEXT,
                    community_id TEXT
                )
            """
            )

    def _build_index_from_entities(self, base_dir):
        entity_dir = os.path.join(base_dir, "entities")
        for file in glob.glob(os.path.join(entity_dir, "shard_*.jsonl")):
            with open(file, encoding="utf-8") as f:
                for line in f:
                    entity = json.loads(line)
                    eid = entity["entity_id"]
                    props = entity["properties"]
                    self._insert(eid, props)

    def _insert(self, entity_id, props):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO entity_index (entity_id, name, type, community_id) VALUES (?, ?, ?, ?)",
                (
                    entity_id,
                    props.get("name"),
                    props.get("type"),
                    props.get("community_id"),
                ),
            )

    def search_by_property(self, key, value):
        cursor = self.conn.cursor()
        try:
            query = f"SELECT entity_id FROM entity_index WHERE {key} = ?"
            cursor.execute(query, (value,))
            print("++++++++++++++++++++++++++")
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.OperationalError:
            return []

    def __del__(self):
        if hasattr(self, "conn"):
            self.conn.close()
