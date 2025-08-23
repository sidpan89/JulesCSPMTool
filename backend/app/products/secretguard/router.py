import typing as t

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import dependencies
from app.users.models import User
from . import crud, schemas, scanners

router = APIRouter()


@router.post("/scans", response_model=schemas.SecretScan, status_code=201, tags=["SecretGuard"])
def trigger_scan(
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
):
    """
    Triggers a new SecretGuard scan.
    """
    scan = crud.create_scan(db=db, tenant_id=current_user.tenant_id)
    mock_findings = scanners.run_mock_scan()

    for finding_data in mock_findings:
        finding_schema = schemas.SecretFindingCreate(**finding_data)
        crud.create_finding(db=db, scan=scan, finding=finding_schema)
    db.commit()

    scan = crud.update_scan_status(db=db, scan=scan, status="completed")
    db.refresh(scan)
    return scan


@router.get("/findings", response_model=t.List[schemas.SecretFinding], tags=["SecretGuard"])
def list_findings(
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all SecretGuard findings for the current user's tenant.
    """
    return crud.get_findings_by_tenant(
        db=db, tenant_id=current_user.tenant_id, skip=skip, limit=limit
    )
