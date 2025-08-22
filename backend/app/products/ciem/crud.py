from sqlalchemy.orm import Session
import uuid

from . import models, schemas

def create_scan(db: Session, tenant_id: uuid.UUID) -> models.IdentityScan:
    """Creates a new identity scan record in the database."""
    scan = models.IdentityScan(tenant_id=tenant_id, status="running")
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

def create_finding(db: Session, scan: models.IdentityScan, finding: schemas.IdentityFindingCreate) -> models.IdentityFinding:
    """Creates a new identity finding record associated with a scan."""
    db_finding = models.IdentityFinding(
        **finding.model_dump(),
        scan_id=scan.id,
        tenant_id=scan.tenant_id
    )
    db.add(db_finding)
    return db_finding

def get_findings_by_tenant(db: Session, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[models.IdentityFinding]:
    """Retrieves all identity findings for a given tenant, with pagination."""
    return db.query(models.IdentityFinding).filter(models.IdentityFinding.tenant_id == tenant_id).offset(skip).limit(limit).all()

def update_scan_status(db: Session, scan: models.IdentityScan, status: str) -> models.IdentityScan:
    """Updates the status of a scan."""
    scan.status = status
    db.commit()
    db.refresh(scan)
    return scan
