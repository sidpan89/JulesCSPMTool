import uuid
from pydantic import BaseModel
from datetime import datetime

# Schemas for Identity Findings
class IdentityFindingBase(BaseModel):
    identity_id: str
    identity_type: str
    issue: str
    severity: str
    description: str

class IdentityFindingCreate(IdentityFindingBase):
    pass

class IdentityFinding(IdentityFindingBase):
    id: uuid.UUID
    scan_id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas for Identity Scans
class IdentityScanBase(BaseModel):
    status: str

class IdentityScanCreate(IdentityScanBase):
    pass

class IdentityScan(IdentityScanBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    findings: list[IdentityFinding] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
