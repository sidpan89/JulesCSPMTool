import uuid
from pydantic import BaseModel, EmailStr

# ==============================================================================
# Base Schemas
# ==============================================================================

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class TenantBase(BaseModel):
    name: str

# ==============================================================================
# Schemas for API Input (Create operations)
# ==============================================================================

class UserCreate(UserBase):
    password: str
    tenant_name: str  # When a new user signs up, they also create their tenant

class TenantCreate(TenantBase):
    pass

# ==============================================================================
# Schemas for API Output (Read operations)
# ==============================================================================

class Tenant(TenantBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class User(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    tenant_id: uuid.UUID
    tenant: Tenant  # Nest tenant information in the user response

    class Config:
        from_attributes = True

# ==============================================================================
# Schemas for Authentication
# ==============================================================================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str | None = None
    tenant_id: str | None = None # Include tenant_id in the token payload for RLS
