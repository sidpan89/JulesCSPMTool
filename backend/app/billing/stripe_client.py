import yaml
from pathlib import Path
import uuid

from app.users.models import Tenant
from app.billing.models import Subscription, SubscriptionStatus
from sqlalchemy.orm import Session

# Load plan data from the YAML file
PLANS_FILE = Path(__file__).parent / "plans.yaml"
with open(PLANS_FILE, 'r') as f:
    PLANS_DATA = yaml.safe_load(f)

def get_plans():
    """Returns all available subscription plans."""
    return PLANS_DATA.get("plans", [])

def get_plan_by_id(plan_id: str):
    """Finds a plan by its ID."""
    for plan in get_plans():
        if plan["id"] == plan_id:
            return plan
    return None

def create_mock_subscription(db: Session, tenant: Tenant, plan_id: str) -> Subscription:
    """
    Simulates the end-to-end process of a Stripe checkout and subscription activation.
    In a real application, this logic would be split between a checkout endpoint
    and a webhook handler.
    """
    plan = get_plan_by_id(plan_id)
    if not plan:
        raise ValueError("Invalid plan ID")

    # Check if a subscription already exists and update it, or create a new one.
    subscription = db.query(Subscription).filter(Subscription.tenant_id == tenant.id).first()

    if not subscription:
        subscription = Subscription(tenant_id=tenant.id)
        db.add(subscription)

    subscription.plan_id = plan_id
    subscription.status = SubscriptionStatus.ACTIVE
    subscription.stripe_subscription_id = f"sub_{uuid.uuid4().hex[:14]}"

    db.commit()
    db.refresh(subscription)

    print(f"Mock subscription '{subscription.stripe_subscription_id}' created and activated for tenant '{tenant.id}' on plan '{plan_id}'.")

    return subscription
