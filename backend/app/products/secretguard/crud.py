from sqlalchemy.orm import Session
import uuid

from . import models, schemas

def create_scan(db: Session, tenant_id: uuid.UUID) -> models.SecretScan:
    """Creates a new secret scan record in the database."""
    scan = models.SecretScan(tenant_id=tenant_id, status="running")
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

def create_finding(db: Session, scan: models.SecretScan, finding: schemas.SecretFindingCreate) -> models.SecretFinding:
    """Creates a new secret finding record associated with a scan."""
    db_finding = models.SecretFinding(
        **finding.model_dump(),
        scan_id=scan.id,
        tenant_id=scan.tenant_id
    )
    db.add(db_finding)
    return db_finding

def get_findings_by_tenant(db: Session, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[models.SecretFinding]:
    """Retrieves all secret findings for a given tenant, with pagination."""
    return db.query(models.SecretFinding).filter(models.SecretFinding.tenant_id == tenant_id).offset(skip).limit(limit).all()

def update_scan_status(db: Session, scan: models.SecretScan, status: str) -> models.SecretScan:
    """Updates the status of a scan."""
    scan.status = status
    db.commit()
    db.refresh(scan)
    return scan
