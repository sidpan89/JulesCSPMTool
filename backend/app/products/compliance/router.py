from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.api import dependencies
from app.users.models import User
from . import generator, schemas

router = APIRouter()


@router.post("/reports", response_class=HTMLResponse, tags=["Compliance"])
def generate_report(
    report_in: schemas.ComplianceReportCreate,
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
):
    """
    Generates a new compliance report.
    """
    # In a real app, you might save the report to the DB and return a report object/ID.
    # For simplicity, we generate and return the HTML directly.
    html_content = generator.generate_html_report(db=db, tenant_id=current_user.tenant_id)
    return HTMLResponse(content=html_content)
