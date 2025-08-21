from sqlalchemy.orm import Session

from app.users import models, schemas
from app.security import get_password_hash

def get_user(db: Session, user_id: str):
    """Retrieves a single user by their ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> models.User | None:
    """Retrieves a single user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user_with_tenant(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Creates a new Tenant and a new User (as the first user for that tenant).
    This function should be called within a single database transaction.
    """
    # 1. Create the Tenant
    new_tenant = models.Tenant(name=user.tenant_name)
    db.add(new_tenant)
    db.flush()  # Use flush to get the generated tenant ID without committing the transaction

    # 2. Create the User
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        tenant_id=new_tenant.id,
        is_active=True,
        is_superuser=True  # The first user of a tenant is a superuser/admin by default
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def create_tenant(db: Session, tenant: schemas.TenantCreate) -> models.Tenant:
    """Creates a new tenant."""
    db_tenant = models.Tenant(name=tenant.name)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant
