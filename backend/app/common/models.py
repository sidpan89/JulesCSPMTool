import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, declared_attr, relationship

# Use timezone-aware UTC datetime
def now_utc():
    return datetime.now(timezone.utc)

Base = declarative_base()

class TimestampMixin:
    """Adds created_at and updated_at columns to a model."""
    created_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now_utc, onupdate=now_utc, nullable=False)

class TenantMixin:
    """Adds a tenant_id foreign key to a model, establishing a link to the Tenant model."""
    @declared_attr
    def tenant_id(cls):
        return Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)

    @declared_attr
    def tenant(cls):
        # This basic relationship can be overridden in child classes if a back_populates is needed.
        return relationship("Tenant")

class AppBase(Base, TimestampMixin):
    """Abstract base model that includes a UUID primary key and timestamps."""
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Optional: A generic way to convert model to dict, excluding internal SQLAlchemy state
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
