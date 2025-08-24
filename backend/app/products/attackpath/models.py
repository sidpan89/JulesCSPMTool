from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.common.models import AppBase, TenantMixin


class AttackPathAnalysis(AppBase, TenantMixin):
    """
    Represents a single Attack Path analysis run.
    """
    __tablename__ = "attackpath_analyses"

    status = Column(String, nullable=False, default="pending")
    nodes = relationship("AttackPathNode", back_populates="analysis", cascade="all, delete-orphan")
    edges = relationship("AttackPathEdge", back_populates="analysis", cascade="all, delete-orphan")


class AttackPathNode(AppBase, TenantMixin):
    """
    Represents a node in the attack path graph (e.g., a resource).
    """
    __tablename__ = "attackpath_nodes"

    analysis_id = Column(UUID(as_uuid=True), ForeignKey("attackpath_analyses.id"), nullable=False)
    analysis = relationship("AttackPathAnalysis", back_populates="nodes")

    node_id = Column(String, nullable=False, index=True)
    node_type = Column(String, nullable=False)
    label = Column(String, nullable=False)
    properties = Column(JSON, nullable=True)


class AttackPathEdge(AppBase, TenantMixin):
    """
    Represents an edge in the attack path graph (i.e., a connection between two nodes).
    """
    __tablename__ = "attackpath_edges"

    analysis_id = Column(UUID(as_uuid=True), ForeignKey("attackpath_analyses.id"), nullable=False)
    analysis = relationship("AttackPathAnalysis", back_populates="edges")

    source_node_id = Column(String, ForeignKey("attackpath_nodes.node_id"), nullable=False)
    target_node_id = Column(String, ForeignKey("attackpath_nodes.node_id"), nullable=False)
    label = Column(String, nullable=False)
    properties = Column(JSON, nullable=True)
