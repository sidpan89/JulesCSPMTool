from pydantic import BaseModel
import uuid
from .models import SubscriptionStatus

class Plan(BaseModel):
    id: str
    name: str
    price: int
    currency: str
    description: str
    features: list[str]

class Subscription(BaseModel):
    id: uuid.UUID
    plan_id: str
    status: SubscriptionStatus
    tenant_id: uuid.UUID

    class Config:
        from_attributes = True

class SubscriptionCreate(BaseModel):
    plan_id: str
