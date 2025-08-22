from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.common.models import AppBase, TenantMixin


class ClusterScan(AppBase, TenantMixin):
    """
    Represents a single KSPM scan run for a Kubernetes cluster.
    """
    __tablename__ = "kspm_scans"

    status = Column(String, nullable=False, default="pending")
    cluster_id = Column(String, nullable=False, index=True)

    findings = relationship("ClusterFinding", back_populates="scan", cascade="all, delete-orphan")


class ClusterFinding(AppBase, TenantMixin):
    """
    Represents a single security finding from a KSPM scan.
    """
    __tablename__ = "kspm_findings"

    scan_id = Column(UUID(as_uuid=True), ForeignKey("kspm_scans.id"), nullable=False)
    scan = relationship("ClusterScan", back_populates="findings")

    resource_id = Column(String, nullable=False, index=True)
    resource_type = Column(String, nullable=False) # e.g., "Pod", "Deployment", "Service"
    namespace = Column(String, nullable=False)
    issue = Column(String, nullable=False, index=True)
    severity = Column(String, nullable=False)
    description = Column(Text, nullable=False)
