from dotenv import load_dotenv

load_dotenv()

import shutil
from pathlib import Path

from fastapi import (
    FastAPI,
    Request,
    UploadFile,
    File,
    Form,
    Body,
    BackgroundTasks,
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
    FileResponse,
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.database import initialize_database

from app.database.system_repository import SystemRepository
from app.database.document_repository import DocumentRepository
from app.database.requirement_repository import RequirementRepository
from app.database.supporting_document_repository import (
    SupportingDocumentRepository,
)

from app.models.document import Document

from app.parsers.document_loader import DocumentLoader
from app.parsers.urs_parser import URSParser

from app.services.document_classifier import DocumentClassifier
from app.services.dashboard_service import DashboardService
from app.services.document_ai_service import DocumentAIService
from app.services.traceability_engine import TraceabilityEngine
from app.services.ai_protocol_generator import AIProtocolGenerator
from app.services.cqvip_engine import CQVIPEngine


app = FastAPI(title="CQVIP")

initialize_database()

templates = Jinja2Templates(
    directory="web/templates"
)

app.mount(
    "/static",
    StaticFiles(directory="web/static"),
    name="static",
)

app.mount(
    "/screenshots",
    StaticFiles(directory="docs/screenshots"),
    name="screenshots",
)

DOCUMENTS = Path("documents")
DOCUMENTS.mkdir(exist_ok=True)

SUPPORTING_DOCS = Path("supporting_documents")
SUPPORTING_DOCS.mkdir(exist_ok=True)

EXPORTS = Path("exports")
EXPORTS.mkdir(exist_ok=True)

PACKAGE = EXPORTS / "Validation_Package.zip"


def load_dashboard():

    requirements = RequirementRepository.all()

    return DashboardService(
        requirements
    ).build()


@app.get("/", response_class=HTMLResponse)
def home():

    return RedirectResponse(
        "/login",
        status_code=303,
    )


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):

    if username == "demo" and password == "demo123":

        return RedirectResponse(
            "/dashboard",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": "Invalid credentials"
        },
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    dashboard = load_dashboard()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "dashboard": dashboard
        },
    )


@app.get("/requirement/{req_id}", response_class=HTMLResponse)
def requirement_workspace(
    request: Request,
    req_id: str,
):

    requirement = RequirementRepository.get(req_id)

    return templates.TemplateResponse(
        request=request,
        name="requirement.html",
        context={
            "requirement": requirement
        },
    )


@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={},
    )


@app.post("/upload-document", response_class=HTMLResponse)
async def upload_document(
    request: Request,
    background_tasks: BackgroundTasks,
    facility: str = Form(...),
    project: str = Form(...),
    system: str = Form(...),
    lifecycle_stage_id: int = Form(...),
    document_type_id: int = Form(...),
    file: UploadFile = File(...),
):
    print("===== UPLOAD ROUTE HIT =====", flush=True)

    print("1. Saving uploaded file", flush=True)

    destination = DOCUMENTS / file.filename

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

        print("2. File saved", flush=True)

    text = DocumentLoader.load(str(destination))

    print("3. Document loaded", flush=True)

    system_id = SystemRepository.get_or_create(
        facility_name=facility,
        project_name=project,
        system_name=system,
    )

    print("4. System created", flush=True)

    metadata = DocumentClassifier.classify(
        file.filename,
        text,
    )

    print("5. Document classified", flush=True)

    document = Document(

        system_id=system_id,

        lifecycle_stage_id=lifecycle_stage_id,

        document_type_id=document_type_id,

        title=file.filename,

        filename=file.filename,

        original_filename=file.filename,

        file_path=str(destination),

        uploaded_by="System",

    )

    document.lifecycle_stage = metadata["lifecycle_stage"]
    document.document_type = metadata["document_type"]

    document = DocumentRepository.create(document)

    print(
        f"Stage={document.lifecycle_stage}, "
        f"Type={document.document_type}, "
        f"Title={document.title}",
        flush=True,
    )

    print("6. Document created", flush=True)

    requirements = URSParser(
        text
    ).extract_requirements()

    print(f"7. Parsed {len(requirements)} requirements", flush=True)

    for req in requirements:
        print("8. Requirements saved", flush=True)

        req.system_id = system_id

        req.document_id = document.id

        req.source_req_id = req.req_id

        req.lifecycle_stage = document.lifecycle_stage

        req.document_type = document.document_type

        req.document_name = document.title

        RequirementRepository.save(req)

    dashboard = DashboardService(
        RequirementRepository.all()
    ).build()

    print("9. Dashboard built", flush=True)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "dashboard": dashboard
        },
    )

@app.post("/api/update-status")
def update_status(data: dict = Body(...)):

    RequirementRepository.update_status(
        data["req_id"],
        data["status"],
    )

    return {
        "success": True
    }


@app.post("/api/assign-owner")
def assign_owner(data: dict = Body(...)):

    RequirementRepository.assign_owner(
        data["req_id"],
        data["assigned_to"],
    )

    return {
        "success": True
    }


@app.post("/api/upload-supporting-document")
async def upload_supporting_document(
    requirement_id: str = Form(...),
    document_type: str = Form(...),
    uploaded_by: str = Form(...),
    file: UploadFile = File(...),
):

    destination = SUPPORTING_DOCS / file.filename

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    requirement = RequirementRepository.get(
        requirement_id
    )

    analysis = DocumentAIService().analyze_document(

        requirement_text=requirement.text,

        file_path=str(destination),

        document_type=document_type,

        lifecycle_stage=getattr(
            requirement,
            "lifecycle_stage",
            "",
        ),

    )

    SupportingDocumentRepository.save(

        requirement_id=requirement_id,

        filename=file.filename,

        document_type=document_type,

        file_path=str(destination),

        uploaded_by=uploaded_by,

        ai_processed=True,

        ai_summary=analysis["summary"],

    )

    return {

        "success": True,

        "analysis": analysis,

    }


@app.post("/api/mark-not-applicable")
def mark_not_applicable(data: dict = Body(...)):

    RequirementRepository.mark_not_applicable(

        req_id=data["req_id"],

        reason=data["reason"],

        justification=data["justification"],

        approved_by=data["approved_by"],

    )

    return {

        "success": True

    }


@app.post("/generate-package")
def generate_package():

    engine = CQVIPEngine()

    engine.load_documents()

    traceability = TraceabilityEngine(
        engine.requirements
    ).build()

    protocol = AIProtocolGenerator(
        engine.requirements
    ).generate()

    import json

    traceability_file = EXPORTS / "traceability.json"

    protocol_file = EXPORTS / "protocol.json"

    with open(
        traceability_file,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            traceability,
            f,
            indent=4,
        )

    with open(
        protocol_file,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            protocol,
            f,
            indent=4,
        )

    package_folder = EXPORTS / "Validation_Package"

    if package_folder.exists():

        shutil.make_archive(

            str(package_folder),

            "zip",

            root_dir=package_folder,

        )

        generated_zip = (
            EXPORTS /
            "Validation_Package.zip"
        )

        if generated_zip.exists():

            return FileResponse(

                generated_zip,

                media_type="application/zip",

                filename="Validation_Package.zip",

            )

    raise RuntimeError(
        "Validation package was not generated."
    )


@app.get("/download")
def download():

    return FileResponse(

        PACKAGE,

        media_type="application/zip",

        filename="Validation_Package.zip",

    )


@app.get("/health")
def health():

    return {

        "status": "ok",

        "application": "CQVIP",

        "version": "3.0",

    }


@app.get("/api/dashboard")
def dashboard_api():

    return load_dashboard()


@app.get("/api/dashboard-version")
def dashboard_version():

    dashboard = load_dashboard()

    return {

        "total": dashboard["total_requirements"],

        "open": dashboard["open_requirements"],

        "readiness": dashboard["quality_compliance_readiness"],

        "inspection": dashboard["inspection_readiness"],

        "phase": dashboard["current_phase"],

    }


@app.get("/api/traceability")
def traceability_api():

    engine = CQVIPEngine()

    engine.load_documents()

    return TraceabilityEngine(
        engine.requirements
    ).build()


@app.get("/api/protocol")
def protocol_api():

    engine = CQVIPEngine()

    engine.load_documents()

    return AIProtocolGenerator(
        engine.requirements
    ).generate()


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "web.main:app",

        host="127.0.0.1",

        port=8000,

        reload=True,

    )