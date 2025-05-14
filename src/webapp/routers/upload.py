from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid

router = APIRouter()
ONGOING = {}

@router.post("/upload")
async def upload_files(
    sop: UploadFile = File(...),
    regs: list[UploadFile] = File(...)
):
    """
    Accept one SOP file and multiple regulatory docs,
    saves them under a new run_id, and returns that ID.
    """
    run_id = str(uuid.uuid4())
    base = f"data/run_{run_id}"
    sop_dir = os.path.join(base, "sop")
    regs_dir = os.path.join(base, "regulatory_docs")
    os.makedirs(sop_dir, exist_ok=True)
    os.makedirs(regs_dir, exist_ok=True)

    sop_path = os.path.join(sop_dir, sop.filename)
    with open(sop_path, "wb") as out:
        shutil.copyfileobj(sop.file, out)

    for reg in regs:
        dest = os.path.join(regs_dir, reg.filename)
        with open(dest, "wb") as out:
            shutil.copyfileobj(reg.file, out)

    ONGOING[run_id] = base
    return {"run_id": run_id}
