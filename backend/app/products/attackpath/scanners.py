def run_mock_scan() -> list[dict]:
    """
    Returns a list of mock resource metadata.
    In a real implementation, this would collect metadata from cloud APIs.
    """
    return [
        {"id": "endpoint-1", "type": "public_endpoint", "label": "Public API Gateway"},
        {"id": "service-1", "type": "service", "label": "Order Service"},
        {"id": "db-1", "type": "database", "label": "Customer Database", "properties": {"critical": True}},
        {"id": "service-2", "type": "service", "label": "Auth Service"},
    ]
