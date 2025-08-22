import uuid
from pydantic import BaseModel
from datetime import datetime

# Schemas for Cluster Findings
class ClusterFindingBase(BaseModel):
    resource_id: str
    resource_type: str
    namespace: str
    issue: str
    severity: str
    description: str

class ClusterFindingCreate(ClusterFindingBase):
    pass

class ClusterFinding(ClusterFindingBase):
    id: uuid.UUID
    scan_id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas for Cluster Scans
class ClusterScanBase(BaseModel):
    status: str
    cluster_id: str

class ClusterScanCreate(BaseModel):
    cluster_id: str

class ClusterScan(ClusterScanBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    findings: list[ClusterFinding] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
