import typing as t
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import dependencies
from app.users.models import User
from app.ai import client as ai_client
from . import crud, schemas, scanners

router = APIRouter()


@router.post("/scans", response_model=schemas.CSPMScan, status_code=201, tags=["CSPM"])
def trigger_scan(
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
):
    """
    Triggers a new CSPM scan.
    NOTE: In a real application, this would be an asynchronous task.
    The endpoint would immediately return a scan object with 'pending' status,
    and a background worker would perform the scan and update the results.
    For this mocked version, we do everything synchronously.
    """
    # 1. Create a new scan record in the database
    scan = crud.create_scan(db=db, tenant_id=current_user.tenant_id)

    # 2. Run the mock scanner to get a list of findings
    mock_findings = scanners.run_mock_scan()

    # 3. Create the findings in the database
    for finding_data in mock_findings:
        finding_schema = schemas.CSPMFindingCreate(**finding_data)
        crud.create_finding(db=db, scan=scan, finding=finding_schema)
    db.commit() # Commit all new findings

    # 4. Update the scan status to 'completed'
    scan = crud.update_scan_status(db=db, scan=scan, status="completed")

    # The scan object returned will be hydrated with the findings through the relationship
    db.refresh(scan)
    return scan


@router.get("/findings", response_model=t.List[schemas.CSPMFinding], tags=["CSPM"])
def list_findings(
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all CSPM findings for the current user's tenant.
    """
    return crud.get_findings_by_tenant(
        db=db, tenant_id=current_user.tenant_id, skip=skip, limit=limit
    )


@router.get("/findings/{finding_id}/explain", response_model=str, tags=["CSPM", "AI"])
def get_explanation(
    finding_id: uuid.UUID,
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
):
    """
    Get a mock AI-powered explanation for a specific finding.
    """
    finding = crud.get_finding_by_id(
        db=db, finding_id=finding_id, tenant_id=current_user.tenant_id
    )
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")

    explanation = ai_client.mock_ai_client.get_finding_explanation(finding)
    return explanation
