import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# ---------------- PATH FIX (CRITICAL FOR WINDOWS) ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
INDEX_FILE = os.path.join(STATIC_DIR, "index.html")
# ----------------------------------------------------------------

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="AI Resume Assistant")

# Serve static assets if needed later
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ---------------- FRONTEND ----------------
@app.get("/")
def serve_index():
    return FileResponse(INDEX_FILE)

# ---------------- MODELS ----------------
class ResumeRequest(BaseModel):
    resume: str
    job_description: str

class JobRequest(BaseModel):
    job_description: str

# ---------------- LLM HELPER ----------------
def ask_llm(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text

# ---------------- API ROUTES ----------------
@app.post("/optimize-resume")
def optimize_resume(data: ResumeRequest):
    prompt = f"""
You are an expert recruiter.
Optimize this resume for the job.
Do NOT invent experience.

RESUME:
{data.resume}

JOB DESCRIPTION:
{data.job_description}
"""
    return {"result": ask_llm(prompt)}

@app.post("/generate-cover-letter")
def generate_cover_letter(data: ResumeRequest):
    prompt = f"""
Write a professional 2-3 paragraph cover letter.

RESUME:
{data.resume}

JOB DESCRIPTION:
{data.job_description}
"""
    return {"result": ask_llm(prompt)}

@app.post("/interview-prep")
def interview_prep(data: JobRequest):
    prompt = f"""
Generate 5 interview questions with STAR guidance.

JOB DESCRIPTION:
{data.job_description}
"""
    return {"result": ask_llm(prompt)}
