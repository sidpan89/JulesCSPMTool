from sqlalchemy.orm import Session
import uuid

from . import models, schemas

def create_analysis(db: Session, tenant_id: uuid.UUID) -> models.AttackPathAnalysis:
    """Creates a new attack path analysis record."""
    analysis = models.AttackPathAnalysis(tenant_id=tenant_id, status="running")
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis

def add_nodes_and_edges(db: Session, analysis: models.AttackPathAnalysis, nodes: list[schemas.AttackPathNodeCreate], edges: list[schemas.AttackPathEdgeCreate]):
    """Adds nodes and edges to an analysis."""
    for node_data in nodes:
        node = models.AttackPathNode(**node_data.model_dump(), analysis_id=analysis.id, tenant_id=analysis.tenant_id)
        db.add(node)

    for edge_data in edges:
        edge = models.AttackPathEdge(**edge_data.model_dump(), analysis_id=analysis.id, tenant_id=analysis.tenant_id)
        db.add(edge)

    db.commit()

def get_latest_analysis_by_tenant(db: Session, tenant_id: uuid.UUID) -> models.AttackPathAnalysis | None:
    """Retrieves the most recent analysis for a given tenant."""
    return db.query(models.AttackPathAnalysis).filter(models.AttackPathAnalysis.tenant_id == tenant_id).order_by(models.AttackPathAnalysis.created_at.desc()).first()

def update_analysis_status(db: Session, analysis: models.AttackPathAnalysis, status: str) -> models.AttackPathAnalysis:
    """Updates the status of an analysis."""
    analysis.status = status
    db.commit()
    db.refresh(analysis)
    return analysis
