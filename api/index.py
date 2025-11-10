import os

from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="api/static"), name="static") # css, js 연결
templates = Jinja2Templates(directory="api/templates") # html(templates) 연결

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/projects")
def projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "contact_location": os.getenv("CONTACT_LOCATION"),
        "contact_email": os.getenv("CONTACT_EMAIL"),

    })

@app.get("/resume", response_class=HTMLResponse)
async def resume_page(request: Request):
    return templates.TemplateResponse("resume.html", {"request": request, "error": None})

@app.post("/resume", response_class=HTMLResponse)
async def resume_download(request: Request, password: str = Form(...)):
    correct_pw = os.getenv("RESUME_PASSWORD")
    if password == correct_pw:
        file_path = "api/static/resume.pdf"
        return FileResponse(path=file_path, filename="Hanyul_Resume.pdf", media_type="application/pdf")
    else:
        return templates.TemplateResponse("resume.html", {"request": request, "error": "비밀번호가 올바르지 않습니다."})