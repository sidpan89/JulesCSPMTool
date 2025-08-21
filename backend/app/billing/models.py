import enum

from sqlalchemy import Column, String, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.common.models import AppBase


class SubscriptionStatus(str, enum.Enum):
    """
    Enum for the status of a subscription.
    """
    ACTIVE = "active"
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"
    TRIALING = "trialing"


class Subscription(AppBase):
    """
    Represents a tenant's subscription to a pricing plan.
    """
    __tablename__ = "subscriptions"

    # The tenant this subscription belongs to. Each tenant has exactly one subscription record.
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, unique=True)

    # The identifier for the plan, e.g., "essential", "growth", "scale".
    plan_id = Column(String, nullable=False)

    # The ID from the payment provider (Stripe).
    stripe_subscription_id = Column(String, unique=True, index=True, nullable=True)

    # The current status of the subscription.
    status = Column(SAEnum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.INCOMPLETE)

    # The back-population for the one-to-one relationship with Tenant.
    tenant = relationship("Tenant", back_populates="subscription")
