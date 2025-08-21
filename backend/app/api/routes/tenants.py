from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.users import models, schemas, crud
from app.api import dependencies

router = APIRouter()

@router.post("/", response_model=schemas.Tenant, status_code=201, tags=["Tenants"])
def create_tenant(
    *,
    db: Session = Depends(dependencies.get_db_from_request),
    tenant_in: schemas.TenantCreate,
    current_user: models.User = Depends(dependencies.get_current_active_superuser),
):
    """
    Create a new tenant.

    This is restricted to superusers. In a multi-tenant application,
    you might have different logic for tenant creation (e.g., via a signup form).
    """
    # In this application, tenants are created during user signup.
    # This endpoint could be used for administrative purposes.
    tenant = crud.create_tenant(db=db, tenant=tenant_in)
    return tenant
