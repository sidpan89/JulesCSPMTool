def run_mock_scan() -> list[dict]:
    """
    Returns a list of mock KSPM findings.
    In a real implementation, this would run tools like kube-bench or Trivy.
    """
    return [
        {
            "resource_id": "pod/insecure-pod",
            "resource_type": "Pod",
            "namespace": "default",
            "issue": "Container running as root",
            "severity": "High",
            "description": "The container 'insecure-container' is running with root privileges.",
        },
        {
            "resource_id": "deployment/dashboard",
            "resource_type": "Deployment",
            "namespace": "kube-system",
            "issue": "Privileged container",
            "severity": "Critical",
            "description": "The deployment 'dashboard' contains a privileged container, which can bypass many security controls.",
        },
        {
            "resource_id": "service/open-redis",
            "resource_type": "Service",
            "namespace": "production",
            "issue": "Exposed to internet",
            "severity": "High",
            "description": "The service 'open-redis' is of type LoadBalancer, exposing it directly to the internet.",
        },
    ]
