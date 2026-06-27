import os
import shutil

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.cqvip_engine import CQVIPEngine


app = FastAPI(title="CQVIP")

templates = Jinja2Templates(directory="web/templates")

app.mount("/static", StaticFiles(directory="web/static"), name="static")

UPLOAD_FOLDER = "documents"
PACKAGE_ZIP = "exports/Validation_Package.zip"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_dashboard_data():
    engine = CQVIPEngine()
    engine.load_documents()

    total_requirements = len(engine.requirements)

    critical_requirements = 0

    for requirement in engine.requirements:
        if requirement.criticality == "Critical":
            critical_requirements += 1

    return {
        "total_requirements": total_requirements,
        "critical_requirements": critical_requirements
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    files = os.listdir(UPLOAD_FOLDER)

    dashboard = get_dashboard_data()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "files": files,
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

    for existing_file in os.listdir(UPLOAD_FOLDER):
        existing_path = os.path.join(UPLOAD_FOLDER, existing_file)

        if os.path.isfile(existing_path):
            os.remove(existing_path)

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return RedirectResponse(
        url="/",
        status_code=303
    )


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