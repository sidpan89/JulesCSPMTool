from . import schemas

def build_graph_from_metadata(metadata: list[dict]) -> tuple[list[schemas.AttackPathNodeCreate], list[schemas.AttackPathEdgeCreate]]:
    """
    Builds a simple graph from a list of resource metadata.
    This is a mock implementation that creates a hardcoded graph structure.
    """
    nodes = []
    for item in metadata:
        nodes.append(schemas.AttackPathNodeCreate(
            node_id=item["id"],
            node_type=item["type"],
            label=item["label"],
            properties=item.get("properties", {})
        ))

    # Hardcoded edges for the mock data
    edges = [
        schemas.AttackPathEdgeCreate(
            source_node_id="endpoint-1",
            target_node_id="service-1",
            label="routes to"
        ),
        schemas.AttackPathEdgeCreate(
            source_node_id="service-1",
            target_node_id="db-1",
            label="accesses"
        ),
        schemas.AttackPathEdgeCreate(
            source_node_id="service-1",
            target_node_id="service-2",
            label="authenticates with"
        ),
    ]

    return nodes, edges
