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
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
    FileResponse,
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.cqvip_engine import CQVIPEngine
from app.services.dashboard_service import DashboardService
from app.services.ai_protocol_generator import AIProtocolGenerator
from app.services.traceability_engine import TraceabilityEngine

app = FastAPI(title="CQVIP")

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

EXPORTS = Path("exports")
EXPORTS.mkdir(exist_ok=True)

PACKAGE = EXPORTS / "Validation_Package.zip"


def load_dashboard():

    engine = CQVIPEngine()

    engine.load_documents()

    return DashboardService(
        engine.requirements
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

    if (
        username == "demo"
        and password == "demo123"
    ):

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
    file: UploadFile = File(...),
):

    destination = DOCUMENTS / file.filename

    with open(destination, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    from app.parsers.document_loader import (
        DocumentLoader,
    )

    from app.parsers.urs_parser import (
        URSParser,
    )

    from app.services.ai_urs_analyzer import (
        AIURSAnalyzer,
    )

    text = DocumentLoader.load_docx(
        str(destination)
    )

    requirements = (
        URSParser(text)
        .extract_requirements()
    )

    payload = [
        {
            "req_id": r.req_id,
            "text": r.text,
        }
        for r in requirements
    ]

    ai_results = AIURSAnalyzer().analyze(
        payload
    )
    for req in requirements:

        ai = next(
            (
                item
                for item in ai_results
                if item["req_id"] == req.req_id
            ),
            {},
        )

        req.category = ai.get("category")

        req.criticality = ai.get("criticality")

        req.recommended_verification = ai.get(
            "verification"
        )

        req.risk = ai.get("risk")

        req.gmp_reference = ai.get(
            "gmp_reference"
        )

        req.acceptance_criteria = ai.get(
            "acceptance_criteria"
        )

        req.suggested_test = ai.get(
            "suggested_test"
        )

        req.protocol_section = ai.get(
            "protocol_section"
        )

        req.test_steps = ai.get(
            "test_steps",
            [],
        )

        req.objective_evidence = ai.get(
            "objective_evidence",
            [],
        )

    dashboard = DashboardService(
        requirements
    ).build()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "dashboard": dashboard
        },
    )
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

    traceability_file = (
        EXPORTS / "traceability.json"
    )

    protocol_file = (
        EXPORTS / "protocol.json"
    )

    import json

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

    engine.run()

    return FileResponse(
        PACKAGE,
        media_type="application/zip",
        filename="Validation_Package.zip",
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
        "version": "2.0"
    }


@app.get("/api/dashboard")
def dashboard_api():

    return load_dashboard()


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