import os

from fastapi import FastAPI, Request
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
