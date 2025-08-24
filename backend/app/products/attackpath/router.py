from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import dependencies
from app.users.models import User
from . import crud, schemas, scanners, graph

router = APIRouter()


@router.post("/analysis", response_model=schemas.AttackPathAnalysis, status_code=201, tags=["AttackPath"])
def trigger_analysis(
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
):
    """
    Triggers a new Attack Path analysis.
    """
    analysis = crud.create_analysis(db=db, tenant_id=current_user.tenant_id)

    metadata = scanners.run_mock_scan()
    nodes, edges = graph.build_graph_from_metadata(metadata)

    crud.add_nodes_and_edges(db=db, analysis=analysis, nodes=nodes, edges=edges)

    analysis = crud.update_analysis_status(db=db, analysis=analysis, status="completed")
    db.refresh(analysis)
    return analysis


@router.get("/analysis", response_model=schemas.AttackPathAnalysis, tags=["AttackPath"])
def get_analysis(
    db: Session = Depends(dependencies.get_db_from_request),
    current_user: User = Depends(dependencies.get_current_user),
):
    """
    Retrieve the latest Attack Path analysis for the current user's tenant.
    """
    return crud.get_latest_analysis_by_tenant(db=db, tenant_id=current_user.tenant_id)
