from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship, declared_attr

from app.common.models import AppBase, TenantMixin

class Tenant(AppBase):
    """
    Represents a tenant in the system. Each tenant is an isolated customer account.
    """
    __tablename__ = "tenants"

    name = Column(String(100), nullable=False)

    # A tenant has many users. If a tenant is deleted, its users are also deleted.
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")

    # A tenant can have one subscription.
    subscription = relationship("Subscription", back_populates="tenant", uselist=False, cascade="all, delete-orphan")


class User(AppBase, TenantMixin):
    """
    Represents a user in the system. Each user belongs to a single tenant.
    """
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # Override the tenant relationship from TenantMixin to add back_populates
    # This completes the bi-directional relationship with Tenant.
    @declared_attr
    def tenant(cls):
        return relationship("Tenant", back_populates="users")
