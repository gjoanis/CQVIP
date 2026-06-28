import os
import shutil

from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse

from app.services.cqvip_engine import CQVIPEngine
from app.services.ai_insights import AIInsights
from app.services.chart_service import ChartService

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="CQVIP")

templates = Jinja2Templates(directory="web/templates")

app.mount("/static", StaticFiles(directory="web/static"), name="static")
app.mount("/screenshots", StaticFiles(directory="docs/screenshots"), name="screenshots")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return JSONResponse({
        "status": "success",
        "filename": file.filename,
        "message": "Document uploaded successfully",
        "next_step": "AI requirement extraction ready"
    })

UPLOAD_FOLDER = "documents"
PACKAGE_ZIP = "exports/Validation_Package.zip"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def safe_get(obj, attr, default=""):
    return getattr(obj, attr, default)


def get_dashboard_data():
    engine = CQVIPEngine()
    engine.load_documents()

    requirements = []

    for requirement in engine.requirements:
        requirements.append({
            "req_id": safe_get(requirement, "req_id"),
            "text": safe_get(requirement, "text"),
            "category": safe_get(requirement, "category"),
            "criticality": safe_get(requirement, "criticality"),
            "recommended": safe_get(
                requirement,
                "recommended_phase",
                safe_get(requirement, "recommended")
            ),
            "verified": safe_get(requirement, "verified", False)
        })

    total_requirements = len(requirements)

    critical_requirements = 0
    open_requirements = 0

    for requirement in requirements:
        if requirement["criticality"] == "Critical":
            critical_requirements += 1

        if requirement["verified"] is False:
            open_requirements += 1

    if total_requirements > 0:
        readiness_score = round(
            ((total_requirements - open_requirements) / total_requirements) * 100
        )
    else:
        readiness_score = 0

    if readiness_score >= 80:
        readiness_status = "Inspection Ready"
    elif readiness_score >= 50:
        readiness_status = "Needs Review"
    else:
        readiness_status = "Not Ready"

    ai = AIInsights(requirements)
    charts = ChartService(requirements)

    return {
        "total_requirements": total_requirements,
        "critical_requirements": critical_requirements,
        "open_requirements": open_requirements,
        "readiness_score": readiness_score,
        "readiness_status": readiness_status,
        "requirements": requirements,
        "charts": charts.build_all_charts(),
        "ai_summary": ai.generate_project_summary(),
        "ai_gap_analysis": ai.generate_gap_analysis(),
        "ai_recommendations": ai.generate_recommendations(),
        "lifecycle": [
            {"stage": "URS", "status": "Complete"},
            {"stage": "FAT", "status": "Complete"},
            {"stage": "SAT", "status": "Complete"},
            {"stage": "Commissioning", "status": "Complete"},
            {"stage": "IQ", "status": "Complete"},
            {"stage": "OQ", "status": "Complete"},
            {"stage": "PQ", "status": "Complete"},
            {"stage": "QSR", "status": "Complete"},
            {"stage": "Released", "status": "Complete"}
        ]
    }

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if username == "demo" and password == "demo123":
        return RedirectResponse(url="/dashboard", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": "Invalid username or password."
        }
    )
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    files = os.listdir(UPLOAD_FOLDER)

    dashboard = {}

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "files": files,
            "dashboard": dashboard
        }
    )
from pathlib import Path
import shutil

UPLOAD_FOLDER = Path("documents")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    dashboard = get_dashboard_data()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "dashboard": dashboard
        }
    )

@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={}
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filepath = UPLOAD_FOLDER / file.filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "filename": file.filename,
        "path": str(filepath)
    }


@app.post("/generate-package")
def generate_package():
    engine = CQVIPEngine()
    engine.run()

    return FileResponse(
        PACKAGE_ZIP,
        media_type="application/zip",
        filename="Validation_Package.zip"
    )


@app.get("/download")
def download_package():
    return FileResponse(
        PACKAGE_ZIP,
        media_type="application/zip",
        filename="Validation_Package.zip"
    )