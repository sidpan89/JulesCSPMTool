import enum

from sqlalchemy import Column, String, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.common.models import AppBase, TenantMixin


class FindingStatus(str, enum.Enum):
    """
    Enum for the status of a security finding.
    """
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class CSPMScan(AppBase, TenantMixin):
    """
    Represents a single CSPM scan run.
    """
    __tablename__ = "cspm_scans"

    status = Column(String, nullable=False, default="pending")

    # A scan has many findings.
    findings = relationship("CSPMFinding", back_populates="scan", cascade="all, delete-orphan")


class CSPMFinding(AppBase, TenantMixin):
    """
    Represents a single security finding from a CSPM scan.
    """
    __tablename__ = "cspm_findings"

    # The scan this finding belongs to.
    scan_id = Column(UUID(as_uuid=True), ForeignKey("cspm_scans.id"), nullable=False)
    scan = relationship("CSPMScan", back_populates="findings")

    resource_id = Column(String, nullable=False, index=True)
    region = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(SAEnum(FindingStatus), nullable=False, default=FindingStatus.OPEN, index=True)

    # A unique identifier for the type of issue, e.g., "cis_1.1" or "prowler_iam_1"
    issue_id = Column(String, nullable=False, index=True)
