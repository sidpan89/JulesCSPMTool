def run_mock_scan() -> list[dict]:
    """
    Returns a list of mock CSPM findings.
    In a real implementation, this would trigger a K8s Job running Prowler/ScoutSuite
    and the results would be fetched from S3/MinIO.
    """
    return [
        {
            "resource_id": "i-0123456789abcdef0",
            "region": "us-east-1",
            "severity": "High",
            "description": "EC2 instance has an internet-facing public IP.",
            "status": "OPEN",
            "issue_id": "prowler_ec2_1"
        },
        {
            "resource_id": "arn:aws:s3:::my-insecure-bucket",
            "region": "global",
            "severity": "Critical",
            "description": "S3 bucket is publicly accessible.",
            "status": "OPEN",
            "issue_id": "prowler_s3_2"
        },
        {
            "resource_id": "sg-abcdef1234567890",
            "region": "us-east-1",
            "severity": "Medium",
            "description": "Security group allows unrestricted ingress on port 22 (SSH).",
            "status": "OPEN",
            "issue_id": "cis_4.1"
        },
        {
            "resource_id": "arn:aws:iam::123456789012:user/my-user",
            "region": "global",
            "severity": "High",
            "description": "IAM user has not rotated access keys in over 90 days.",
            "status": "ACKNOWLEDGED",
            "issue_id": "cis_1.3"
        },
        {
            "resource_id": "vol-0123456789abcdef0",
            "region": "us-west-2",
            "severity": "Low",
            "description": "EBS volume is unencrypted.",
            "status": "RESOLVED",
            "issue_id": "prowler_ebs_1"
        }
    ]
