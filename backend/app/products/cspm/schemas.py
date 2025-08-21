import uuid
from pydantic import BaseModel
from datetime import datetime
from .models import FindingStatus

# Schemas for Findings
class CSPMFindingBase(BaseModel):
    resource_id: str
    region: str
    severity: str
    description: str
    status: FindingStatus
    issue_id: str

class CSPMFindingCreate(CSPMFindingBase):
    pass

class CSPMFinding(CSPMFindingBase):
    id: uuid.UUID
    scan_id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas for Scans
class CSPMScanBase(BaseModel):
    status: str

class CSPMScanCreate(CSPMScanBase):
    pass

class CSPMScan(CSPMScanBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    findings: list[CSPMFinding] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
