import typing as t

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import dependencies
from app.users.models import User
from . import crud, schemas, scanners

router = APIRouter()


@router.post("/scans", response_model=schemas.ClusterScan, status_code=201, tags=["KSPM"])
def trigger_scan(
    scan_in: schemas.ClusterScanCreate,
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
):
    """
    Triggers a new KSPM scan for a specific cluster.
    """
    scan = crud.create_scan(db=db, tenant_id=current_user.tenant_id, scan_in=scan_in)
    mock_findings = scanners.run_mock_scan()

    for finding_data in mock_findings:
        finding_schema = schemas.ClusterFindingCreate(**finding_data)
        crud.create_finding(db=db, scan=scan, finding=finding_schema)
    db.commit()

    scan = crud.update_scan_status(db=db, scan=scan, status="completed")
    db.refresh(scan)
    return scan


@router.get("/findings", response_model=t.List[schemas.ClusterFinding], tags=["KSPM"])
def list_findings(
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all KSPM findings for the current user's tenant.
    """
    return crud.get_findings_by_tenant(
        db=db, tenant_id=current_user.tenant_id, skip=skip, limit=limit
    )
