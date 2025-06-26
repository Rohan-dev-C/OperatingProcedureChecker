import os, shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from src.cli import run_pipeline

router = APIRouter()

@router.post("/upload-sop/")
async def upload_sop(file: UploadFile = File(...)):
    os.makedirs("data/sop", exist_ok=True)
    path = os.path.join("data/sop", file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": f"SOP uploaded: {file.filename}"}

@router.post("/upload-reg/")
async def upload_reg(file: UploadFile = File(...)):
    os.makedirs("data/regulatory_docs", exist_ok=True)
    path = os.path.join("data/regulatory_docs", file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": f"Regulatory file uploaded: {file.filename}"}

@router.post("/run-analysis/")
async def run_compliance():
    run_pipeline("data/sop", "data/regulatory_docs")
    return {"message": "Analysis complete"}

@router.get("/report", response_class=HTMLResponse)
async def get_report():
    report_path = "compliance_report.md"
    if not os.path.exists(report_path):
        return HTMLResponse("No report generated yet.", status_code=404)
    import markdown
    text = open(report_path, "r", encoding="utf-8").read()
    return HTMLResponse(markdown.markdown(text, extensions=["extra"]))
