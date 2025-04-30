import json
import os


# Recreate the fixture generator
def create_test_graph_fixture(base_dir="test_graph_fixture"):
    # Create necessary directories
    os.makedirs(os.path.join(base_dir, "logs"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "entities"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "relations"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "adjacency"), exist_ok=True)

    # Entities
    entities = [
        {
            "entity_id": 1,
            "properties": {
                "name": "Alice",
                "type": "Person",
                "community_id": "team_alpha",
            },
            "update_time": "2025-04-28T12:00:00Z",
        },
        {
            "entity_id": 2,
            "properties": {
                "name": "Bob",
                "type": "Person",
                "community_id": "team_alpha",
            },
            "update_time": "2025-04-28T12:01:00Z",
        },
        {
            "entity_id": 3,
            "properties": {
                "name": "Charlie",
                "type": "Person",
                "community_id": "team_beta",
            },
            "update_time": "2025-04-28T12:02:00Z",
        },
    ]
    with open(
        os.path.join(base_dir, "entities", "shard_0.jsonl"), "w", encoding="utf-8"
    ) as f:
        for entity in entities:
            f.write(json.dumps(entity) + "\n")

    # Relations
    relations = [
        {
            "relation_id": 101,
            "source_id": 1,
            "target_id": 2,
            "properties": {"type": "FRIENDS_WITH"},
            "update_time": "2025-04-28T12:10:00Z",
        },
        {
            "relation_id": 102,
            "source_id": 2,
            "target_id": 3,
            "properties": {"type": "COWORKERS_WITH"},
            "update_time": "2025-04-28T12:12:00Z",
        },
    ]
    with open(
        os.path.join(base_dir, "relations", "shard_0.jsonl"),
        "w",
        encoding="utf-8",
    ) as f:
        for relation in relations:
            f.write(json.dumps(relation) + "\n")

    # Adjacency
    adjacency = [
        {"entity_id": 1, "relations": [101]},
        {"entity_id": 2, "relations": [102]},
    ]
    with open(
        os.path.join(base_dir, "adjacency", "adjacency.jsonl"), "w", encoding="utf-8"
    ) as f:
        for adj in adjacency:
            f.write(json.dumps(adj) + "\n")

    print(f"Test graph fixture created under: {base_dir}")


# Run it
create_test_graph_fixture()
