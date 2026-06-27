from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.cqvip_engine import CQVIPEngine

from fastapi import UploadFile, File
import shutil
import os

UPLOAD_FOLDER = "documents"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = FastAPI(title="CQVIP")

templates = Jinja2Templates(directory="web/templates")

app.mount("/static", StaticFiles(directory="web/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/generate-package")
def generate_package():
    engine = CQVIPEngine()
    engine.run()

    return FileResponse(
        "exports/Validation_Package.zip",
        media_type="application/zip",
        filename="Validation_Package.zip"
    )

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Upload successful",
        "filename": file.filename
    }