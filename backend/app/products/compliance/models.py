from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.common.models import AppBase, TenantMixin


class ComplianceReport(AppBase, TenantMixin):
    """
    Represents a single generated compliance report.
    """
    __tablename__ = "compliance_reports"

    report_type = Column(String, nullable=False) # e.g., "CIS_Benchmark_v1.4"
    status = Column(String, nullable=False, default="pending")
    content = Column(Text, nullable=True) # The generated report content (HTML)
