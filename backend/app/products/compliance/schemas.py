import uuid
from pydantic import BaseModel
from datetime import datetime

class ComplianceReportBase(BaseModel):
    report_type: str
    status: str
    content: str | None = None

class ComplianceReportCreate(BaseModel):
    report_type: str

class ComplianceReport(ComplianceReportBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
