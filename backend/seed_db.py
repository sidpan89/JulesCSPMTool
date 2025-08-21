import uuid
from sqlalchemy.orm import Session
from app.common.db import SessionLocal
from app.users.models import User, Tenant
from app.billing.models import Subscription, SubscriptionStatus
from app.products.cspm.models import CSPMScan, CSPMFinding, FindingStatus
from app.security import get_password_hash

def seed_db(db: Session):
    print("Seeding database...")

    # Check if user already exists
    user = db.query(User).filter(User.email == "testuser@example.com").first()
    if user:
        print("User 'testuser@example.com' already exists. Seeding aborted.")
        return

    # 1. Create Tenant
    tenant = Tenant(name="Test Tenant Inc.", id=uuid.uuid4())
    db.add(tenant)
    db.flush()
    print(f"Created tenant: {tenant.name}")

    # 2. Create User
    hashed_password = get_password_hash("password123")
    user = User(
        id=uuid.uuid4(),
        email="testuser@example.com",
        full_name="Test User",
        hashed_password=hashed_password,
        tenant_id=tenant.id,
        is_superuser=True
    )
    db.add(user)
    print(f"Created user: {user.email}")

    # 3. Create Subscription
    subscription = Subscription(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        plan_id="growth",
        status=SubscriptionStatus.ACTIVE,
        stripe_subscription_id="sub_mock_seeded"
    )
    db.add(subscription)
    print(f"Created subscription for tenant on plan: {subscription.plan_id}")

    # 4. Create CSPM Scan
    scan = CSPMScan(id=uuid.uuid4(), tenant_id=tenant.id, status="completed")
    db.add(scan)
    print(f"Created CSPM scan: {scan.id}")

    # 5. Create CSPM Findings
    findings_data = [
        { "resource_id": "i-0123456789abcdef0", "region": "us-east-1", "severity": "High", "description": "EC2 instance has an internet-facing public IP.", "status": FindingStatus.OPEN, "issue_id": "prowler_ec2_1" },
        { "resource_id": "arn:aws:s3:::my-insecure-bucket", "region": "global", "severity": "Critical", "description": "S3 bucket is publicly accessible.", "status": FindingStatus.OPEN, "issue_id": "prowler_s3_2" },
    ]

    for finding_data in findings_data:
        finding = CSPMFinding(
            id=uuid.uuid4(),
            scan_id=scan.id,
            tenant_id=tenant.id,
            **finding_data
        )
        db.add(finding)

    print(f"Created {len(findings_data)} CSPM findings.")

    db.commit()
    print("Database seeding complete.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
