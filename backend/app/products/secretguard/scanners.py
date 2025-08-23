def run_mock_scan() -> list[dict]:
    """
    Returns a list of mock SecretGuard findings.
    In a real implementation, this would scan code repos, storage blobs, etc.
    """
    return [
        {
            "location": "s3://my-company-blobs/config/prod.env",
            "secret_type": "AWS Access Key",
            "severity": "Critical",
            "details": "Found AWS access key ID 'AKIAIOSFODNN7EXAMPLE' in a public S3 bucket.",
        },
        {
            "location": "github.com/my-company/my-repo/src/config.js",
            "secret_type": "API Key",
            "severity": "High",
            "details": "Found a hardcoded API key for a third-party service.",
        },
        {
            "location": "Azure Key Vault: 'kv-prod-123'",
            "secret_type": "Certificate",
            "severity": "Medium",
            "details": "Certificate 'self-signed-cert' is due to expire in 15 days.",
        },
    ]
