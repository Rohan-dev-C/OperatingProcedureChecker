# src/webapp/main.py

import pathlib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from src.webapp.routers import compliance

app = FastAPI()
app.include_router(compliance.router)

# Resolve the directory containing this file
HERE = pathlib.Path(__file__).parent

# Mount /static → src/webapp/static
static_dir = HERE / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Serve index.html at /
@app.get("/", response_class=FileResponse)
async def serve_index():
    index_path = static_dir / "index.html"
    return str(index_path)
