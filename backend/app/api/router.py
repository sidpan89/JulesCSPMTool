from fastapi import APIRouter

from app.api.routes import auth, tenants, subscriptions
from app.products.cspm.router import router as cspm_router
from app.products.ciem.router import router as ciem_router
from app.products.kspm.router import router as kspm_router
from app.products.secretguard.router import router as secretguard_router

api_router = APIRouter()

# Core Services
api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(subscriptions.router, tags=["Billing"])

# Product-specific routes will be added here
api_router.include_router(cspm_router, prefix="/cspm", tags=["CSPM-Lite"])
api_router.include_router(ciem_router, prefix="/ciem", tags=["CIEM-Lite"])
api_router.include_router(kspm_router, prefix="/kspm", tags=["KSPM-Lite"])
api_router.include_router(secretguard_router, prefix="/secretguard", tags=["SecretGuard"])
