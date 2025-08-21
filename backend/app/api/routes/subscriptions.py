import typing as t

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import dependencies
from app.users.models import User
from app.billing import stripe_client, schemas

router = APIRouter()


@router.get("/plans", response_model=t.List[schemas.Plan], tags=["Billing"])
def list_plans():
    """
    Get a list of all available subscription plans.
    """
    return stripe_client.get_plans()


@router.post("/subscriptions", response_model=schemas.Subscription, status_code=201, tags=["Billing"])
def create_subscription(
    subscription_in: schemas.SubscriptionCreate,
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
):
    """
    Create a (mock) subscription for the current user's tenant.
    """
    tenant = current_user.tenant
    if not tenant:
        # This should not happen if the user is authenticated correctly
        raise HTTPException(status_code=404, detail="Tenant not found for user")

    try:
        subscription = stripe_client.create_mock_subscription(
            db=db, tenant=tenant, plan_id=subscription_in.plan_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return subscription
