from sqlalchemy.orm import Session
import uuid

from app.products.cspm import crud as cspm_crud
from app.products.ciem import crud as ciem_crud
# Import other product cruds as they are created

def generate_html_report(db: Session, tenant_id: uuid.UUID) -> str:
    """
    Generates a simple HTML compliance report for a given tenant.
    """
    cspm_findings = cspm_crud.get_findings_by_tenant(db, tenant_id=tenant_id)
    ciem_findings = ciem_crud.get_findings_by_tenant(db, tenant_id=tenant_id)

    html = "<html><head><title>Compliance Report</title>"
    html += "<style>body { font-family: sans-serif; } table { border-collapse: collapse; width: 100%; } th, td { border: 1px solid #ddd; padding: 8px; text-align: left; } th { background-color: #f2f2f2; }</style>"
    html += "</head><body>"
    html += f"<h1>Compliance Report for Tenant {tenant_id}</h1>"

    # CSPM Findings
    html += "<h2>CSPM Findings</h2>"
    if cspm_findings:
        html += "<table><tr><th>Resource ID</th><th>Severity</th><th>Description</th></tr>"
        for f in cspm_findings:
            html += f"<tr><td>{f.resource_id}</td><td>{f.severity}</td><td>{f.description}</td></tr>"
        html += "</table>"
    else:
        html += "<p>No CSPM findings.</p>"

    # CIEM Findings
    html += "<h2>CIEM Findings</h2>"
    if ciem_findings:
        html += "<table><tr><th>Identity ID</th><th>Issue</th><th>Severity</th></tr>"
        for f in ciem_findings:
            html += f"<tr><td>{f.identity_id}</td><td>{f.issue}</td><td>{f.severity}</td></tr>"
        html += "</table>"
    else:
        html += "<p>No CIEM findings.</p>"

    html += "</body></html>"

    return html
