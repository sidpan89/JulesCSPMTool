def run_mock_scan() -> list[dict]:
    """
    Returns a list of mock CIEM findings.
    In a real implementation, this would query Azure AD Graph API.
    """
    return [
        {
            "identity_id": "arn:aws:iam::123456789012:role/AdminRole",
            "identity_type": "role",
            "issue": "Overly Broad Permissions",
            "severity": "Critical",
            "description": "The role 'AdminRole' has 'AdministratorAccess' policy attached, granting unrestricted access to all resources.",
        },
        {
            "identity_id": "user@example.com",
            "identity_type": "user",
            "issue": "Missing MFA",
            "severity": "High",
            "description": "The user 'user@example.com' does not have Multi-Factor Authentication (MFA) enabled.",
        },
        {
            "identity_id": "app-service-principal-id",
            "identity_type": "service_principal",
            "issue": "Unused Credentials",
            "severity": "Medium",
            "description": "The service principal 'app-service-principal-id' has credentials that have not been used in over 90 days.",
        },
    ]
