import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Any

# Schemas for Nodes
class AttackPathNodeBase(BaseModel):
    node_id: str
    node_type: str
    label: str
    properties: dict[str, Any] | None = None

class AttackPathNodeCreate(AttackPathNodeBase):
    pass

class AttackPathNode(AttackPathNodeBase):
    id: uuid.UUID
    analysis_id: uuid.UUID

    class Config:
        from_attributes = True

# Schemas for Edges
class AttackPathEdgeBase(BaseModel):
    source_node_id: str
    target_node_id: str
    label: str
    properties: dict[str, Any] | None = None

class AttackPathEdgeCreate(AttackPathEdgeBase):
    pass

class AttackPathEdge(AttackPathEdgeBase):
    id: uuid.UUID
    analysis_id: uuid.UUID

    class Config:
        from_attributes = True

# Schemas for Analysis
class AttackPathAnalysisBase(BaseModel):
    status: str

class AttackPathAnalysisCreate(BaseModel):
    pass

class AttackPathAnalysis(AttackPathAnalysisBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    nodes: list[AttackPathNode] = []
    edges: list[AttackPathEdge] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
