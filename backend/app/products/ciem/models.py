from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.common.models import AppBase, TenantMixin


class IdentityScan(AppBase, TenantMixin):
    """
    Represents a single CIEM scan run.
    """
    __tablename__ = "ciem_scans"

    status = Column(String, nullable=False, default="pending")

    # A scan has many findings.
    findings = relationship("IdentityFinding", back_populates="scan", cascade="all, delete-orphan")


class IdentityFinding(AppBase, TenantMixin):
    """
    Represents a single security finding from a CIEM scan.
    """
    __tablename__ = "ciem_findings"

    # The scan this finding belongs to.
    scan_id = Column(UUID(as_uuid=True), ForeignKey("ciem_scans.id"), nullable=False)
    scan = relationship("IdentityScan", back_populates="findings")

    identity_id = Column(String, nullable=False, index=True) # e.g., user ARN, service principal ID
    identity_type = Column(String, nullable=False) # e.g., "user", "role", "service_principal"
    issue = Column(String, nullable=False, index=True) # e.g., "Overly Broad Permissions", "Missing MFA"
    severity = Column(String, nullable=False)
    description = Column(Text, nullable=False)
