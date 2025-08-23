import uuid
from pydantic import BaseModel
from datetime import datetime

# Schemas for Secret Findings
class SecretFindingBase(BaseModel):
    location: str
    secret_type: str
    severity: str
    details: str

class SecretFindingCreate(SecretFindingBase):
    pass

class SecretFinding(SecretFindingBase):
    id: uuid.UUID
    scan_id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas for Secret Scans
class SecretScanBase(BaseModel):
    status: str

class SecretScanCreate(BaseModel):
    pass

class SecretScan(SecretScanBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    findings: list[SecretFinding] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
