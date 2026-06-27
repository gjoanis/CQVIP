from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.cqvip_engine import CQVIPEngine


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