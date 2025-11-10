import os

from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

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

@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    contact_info = {
        "location": os.getenv("CONTACT_LOCATION"),
        "email": os.getenv("CONTACT_EMAIL"),
    }
    return templates.TemplateResponse(
        "contact.html",
        {"request": request, "success": None, "error": None, **contact_info},
    )

@app.post("/contact", response_class=HTMLResponse)
async def send_contact_email(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    contact_email = os.getenv("CONTACT_EMAIL")

    contact_info = {
        "location": os.getenv("CONTACT_LOCATION"),
        "email": os.getenv("CONTACT_EMAIL"),
    }

    try:
        subject_admin = f"[이력서 문의] {name}님으로부터의 메시지"
        body_admin = f"""
        📩 이름: {name}
        📧 이메일: {email}

        💬 메시지:
        {message}
        """

        msg_admin = MIMEText(body_admin, "plain", "utf-8")
        msg_admin["Subject"] = subject_admin
        msg_admin["From"] = smtp_user
        msg_admin["To"] = contact_email

        # 2️⃣ 사용자 자동 회신 메일
        subject_reply = "한율님에게 문의가 접수되었습니다."
        body_reply = f"""
        안녕하세요, {name}님.

        문의해주셔서 감사합니다.
        보내주신 내용이 정상적으로 접수되었습니다. 🙂
        48시간 이내에 답변드리도록 하겠습니다.

        - Hanyul
        """

        msg_reply = MIMEText(body_reply, "plain", "utf-8")
        msg_reply["Subject"] = subject_reply
        msg_reply["From"] = smtp_user
        msg_reply["To"] = email

        # ✅ 메일 전송
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            # 관리자에게 전달
            server.send_message(msg_admin)
            # 사용자에게 자동 회신
            server.send_message(msg_reply)

        return templates.TemplateResponse(
            "contact.html",
            {"request": request, "success": True, "error": None, **contact_info},
        )

    except Exception as e:
        print(f"Email send error: {e}")
        return templates.TemplateResponse(
            "contact.html",
            {"request": request, "success": None, "error": True, **contact_info},
        )

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