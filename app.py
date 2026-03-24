from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional
import mammoth
from fastapi.responses import HTMLResponse

from core import generate_resume, export_resume, Resume  # ✅ FIXED

app = FastAPI(title="AI Resume Builder API")


class ResumeInput(BaseModel):
    name: str
    email: str
    phone: str
    skills: Optional[str] = None
    education: Optional[str] = None
    projects: Optional[str] = None
    experience: Optional[str] = None
    clubs: Optional[str] = None



@app.post("/generate")
def generate(data: ResumeInput):
    try:
        resume_dict = generate_resume(data.model_dump())
        return {"success": True, "resume": resume_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def resume_to_html(resume: Resume) -> str:
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Calibri, sans-serif;
                max-width: 800px;
                margin: auto;
                padding: 40px;
                line-height: 1.6;
                color: #222;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 5px;
                color: #1f3864;
            }}
            .contact {{
                text-align: center;
                font-size: 14px;
                color: #555;
                margin-bottom: 10px;
            }}
            h2 {{
                border-bottom: 2px solid #2E74B5;
                margin-top: 20px;
                text-transform: uppercase;
                font-size: 14px;
            }}
            .section {{
                margin-bottom: 10px;
            }}
            ul {{
                margin: 5px 0 10px 20px;
            }}
            .muted {{
                color: #666;
                font-size: 13px;
            }}
        </style>
    </head>
    <body>

    <h1>{resume.name}</h1>
    <div class="contact">{resume.email} | {resume.phone}</div>

    {"<h2>Professional Summary</h2><p>" + resume.summary + "</p>" if resume.summary else ""}

    {"<h2>Skills</h2><p>" + " • ".join(resume.skills) + "</p>" if resume.skills else ""}

    {"<h2>Education</h2>" + "".join([
        f"<p><b>{e.degree}</b> — {e.institution} <span class='muted'>| {e.year} | {e.grade or ''}</span></p>"
        for e in resume.education
    ]) if resume.education else ""}

    {"<h2>Projects</h2>" + "".join([
        f"<p><b>{p.name}</b>" +
        (f" <span class='muted'>| Tech: {', '.join(p.technologies)}</span>" if p.technologies else "") +
        "</p><ul>" +
        "".join([f"<li>{d}</li>" for d in p.description]) +
        "</ul>"
        for p in resume.projects
    ]) if resume.projects else ""}

    {"<h2>Experience</h2>" + "".join([
        f"<p><b>{e.role} — {e.company}</b> <span class='muted'>| {e.duration}</span></p><ul>" +
        "".join([f"<li>{d}</li>" for d in e.description]) +
        "</ul>"
        for e in resume.experience
    ]) if resume.experience else ""}

    {"<h2>Clubs & Activities</h2>" + "".join([
        f"<p><b>{c.name}</b> — {c.role}</p><p>{c.description or ''}</p>"
        for c in resume.clubs
    ]) if resume.clubs else ""}

    </body>
    </html>
    """


@app.post("/preview-docx", response_class=HTMLResponse)
def preview(data: ResumeInput):
    resume_dict = generate_resume(data.model_dump())
    resume = Resume.model_validate(resume_dict)

    return resume_to_html(resume)


@app.post("/download")
def download(data: ResumeInput, format: str = "docx"):
    resume_dict = generate_resume(data.model_dump())
    resume = Resume.model_validate(resume_dict)

    file_path = export_resume(resume, format=format)

    return FileResponse(
        file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )