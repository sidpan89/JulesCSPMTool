from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.common.models import AppBase, TenantMixin


class SecretScan(AppBase, TenantMixin):
    """
    Represents a single SecretGuard scan run.
    """
    __tablename__ = "secret_scans"

    status = Column(String, nullable=False, default="pending")

    findings = relationship("SecretFinding", back_populates="scan", cascade="all, delete-orphan")


class SecretFinding(AppBase, TenantMixin):
    """
    Represents a single secret finding from a SecretGuard scan.
    """
    __tablename__ = "secret_findings"

    scan_id = Column(UUID(as_uuid=True), ForeignKey("secret_scans.id"), nullable=False)
    scan = relationship("SecretScan", back_populates="findings")

    location = Column(String, nullable=False, index=True) # e.g., file path, URL, blob storage URI
    secret_type = Column(String, nullable=False) # e.g., "API Key", "Password", "Private Key"
    severity = Column(String, nullable=False)
    details = Column(Text, nullable=False)
