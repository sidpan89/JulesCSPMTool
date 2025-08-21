from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.settings import settings
from jose import jwt, JWTError

from app.api.router import api_router
from app.common.db import SessionLocal, set_tenant_id_for_rls

app = FastAPI(
    title="AI Cloud Security Suite",
    description="An AI-powered, multi-tenant cloud security platform.",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set all CORS enabled origins
if settings.ENVIRONMENT == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.middleware("http")
async def rls_db_session_middleware(request: Request, call_next):
    """
    FastAPI middleware to handle DB session lifecycle and set tenant for RLS.
    """
    db = SessionLocal()
    request.state.db = db

    tenant_id = None
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            tenant_id = payload.get("tenant_id")
        except JWTError:
            # If token is invalid, we proceed without tenant context.
            # Protected routes will fail later during authentication.
            pass

    try:
        if tenant_id:
            # NOTE: RLS is a PostgreSQL-specific feature.
            # This is disabled for the SQLite workaround.
            # set_tenant_id_for_rls(db, tenant_id)
            pass

        response = await call_next(request)
    finally:
        db.close()

    return response


app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health Check"], include_in_schema=False)
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok", "title": app.title, "version": app.version}
