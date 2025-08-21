from sqlalchemy.orm import Session
import uuid

from . import models, schemas

def create_scan(db: Session, tenant_id: uuid.UUID) -> models.CSPMScan:
    """Creates a new scan record in the database."""
    scan = models.CSPMScan(tenant_id=tenant_id, status="running")
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

def create_finding(db: Session, scan: models.CSPMScan, finding: schemas.CSPMFindingCreate) -> models.CSPMFinding:
    """Creates a new finding record associated with a scan."""
    db_finding = models.CSPMFinding(
        **finding.model_dump(),
        scan_id=scan.id,
        tenant_id=scan.tenant_id
    )
    db.add(db_finding)
    # The calling function should handle the commit after all findings are added.
    return db_finding

def get_findings_by_tenant(db: Session, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[models.CSPMFinding]:
    """Retrieves all findings for a given tenant, with pagination."""
    return db.query(models.CSPMFinding).filter(models.CSPMFinding.tenant_id == tenant_id).offset(skip).limit(limit).all()

def get_finding_by_id(db: Session, finding_id: uuid.UUID, tenant_id: uuid.UUID) -> models.CSPMFinding | None:
    """Retrieves a single finding by its ID, ensuring it belongs to the correct tenant."""
    return db.query(models.CSPMFinding).filter(models.CSPMFinding.id == finding_id, models.CSPMFinding.tenant_id == tenant_id).first()

def update_scan_status(db: Session, scan: models.CSPMScan, status: str) -> models.CSPMScan:
    """Updates the status of a scan."""
    scan.status = status
    db.commit()
    db.refresh(scan)
    return scan
