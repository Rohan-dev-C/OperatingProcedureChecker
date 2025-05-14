from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from src.webapp.routers.upload import ONGOING
import os

router = APIRouter()
templates = Jinja2Templates(directory="src/webapp/templates")

@router.get("/report/{run_id}")
async def get_report(request: Request, run_id: str):
    """
    Render the compliance report for a completed run_id.
    Expects a Markdown file at data/run_<run_id>/compliance_report.md
    and uses a Jinja2 template 'report.html'.
    """
    if run_id not in ONGOING:
        raise HTTPException(status_code=404, detail="Run ID not found")

    base = ONGOING[run_id]
    md_path = os.path.join(base, "compliance_report.md")
    if not os.path.exists(md_path):
        raise HTTPException(status_code=404, detail="Report not yet generated")

    with open(md_path, "r") as f:
        report_md = f.read()

    return templates.TemplateResponse(
        "report.html",
        {"request": request, "report_md": report_md, "run_id": run_id}
    )
