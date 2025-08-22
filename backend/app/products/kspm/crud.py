from sqlalchemy.orm import Session
import uuid

from . import models, schemas

def create_scan(db: Session, tenant_id: uuid.UUID, scan_in: schemas.ClusterScanCreate) -> models.ClusterScan:
    """Creates a new cluster scan record in the database."""
    scan = models.ClusterScan(
        tenant_id=tenant_id,
        cluster_id=scan_in.cluster_id,
        status="running"
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

def create_finding(db: Session, scan: models.ClusterScan, finding: schemas.ClusterFindingCreate) -> models.ClusterFinding:
    """Creates a new cluster finding record associated with a scan."""
    db_finding = models.ClusterFinding(
        **finding.model_dump(),
        scan_id=scan.id,
        tenant_id=scan.tenant_id
    )
    db.add(db_finding)
    return db_finding

def get_findings_by_tenant(db: Session, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[models.ClusterFinding]:
    """Retrieves all cluster findings for a given tenant, with pagination."""
    return db.query(models.ClusterFinding).filter(models.ClusterFinding.tenant_id == tenant_id).offset(skip).limit(limit).all()

def update_scan_status(db: Session, scan: models.ClusterScan, status: str) -> models.ClusterScan:
    """Updates the status of a scan."""
    scan.status = status
    db.commit()
    db.refresh(scan)
    return scan
