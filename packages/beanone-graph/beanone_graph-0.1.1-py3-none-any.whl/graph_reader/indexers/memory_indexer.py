import glob
import json
import os

from .base_indexer import BaseIndexer


class MemoryIndexer(BaseIndexer):
    def __init__(self, base_dir):
        self.map = {}
        # Read all entity files and build the index
        entity_dir = os.path.join(base_dir, "entities")
        if os.path.exists(entity_dir):
            for file in glob.glob(os.path.join(entity_dir, "shard_*.jsonl")):
                with open(file, encoding="utf-8") as f:
                    for line in f:
                        entity = json.loads(line)
                        entity_id = entity["entity_id"]
                        self.map[entity_id] = entity["properties"]

    def search_by_property(self, key, value):
        return [
            eid
            for eid, props in self.map.items()
            if key in props and props[key] == value
        ]
