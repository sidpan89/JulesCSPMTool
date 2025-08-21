from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.settings import settings

# Create the SQLAlchemy engine
# pool_pre_ping=True checks connections for liveness before handing them out from the pool.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def set_tenant_id_for_rls(db: Session, tenant_id: str) -> None:
    """
    Sets the 'app.current_tenant' variable for the current database session.
    This is used by the RLS policies in PostgreSQL.
    """
    # This is a synchronous execution.
    db.execute(text("SELECT set_config('app.current_tenant', :tenant_id, false)"), {'tenant_id': tenant_id})
