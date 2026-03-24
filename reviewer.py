import os
import json
import requests
from typing import List
from enum import Enum

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError



load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL ="meta-llama/llama-3-8b-instruct"

if not OPENROUTER_API_KEY:
    raise ValueError("❌ Missing OPENROUTER_API_KEY in .env")




class StrengthLevel(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"


class SectionScore(BaseModel):
    section_name: str
    score: int = Field(ge=0, le=10)
    feedback: str
    suggestions: List[str]


class ATSAnalysis(BaseModel):
    ats_score: int = Field(ge=0, le=100)
    missing_keywords: List[str]
    formatting_issues: List[str]


class ResumeReviewResult(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    grade: str
    strength_level: StrengthLevel
    section_scores: List[SectionScore]
    top_strengths: List[str]
    critical_gaps: List[str]
    quick_wins: List[str]
    ats_analysis: ATSAnalysis
    recruiter_verdict: str
    rewrite_hints: List[str]




SYSTEM_PROMPT = """
You are an expert resume reviewer with 10+ years of hiring experience.

Return ONLY valid JSON. No markdown. No explanation.

Follow this schema strictly:

{
  "overall_score": int (0-100),
  "grade": "A|B|C|D|F",
  "strength_level": "strong|moderate|weak",
  "section_scores": [
    {
      "section_name": string,
      "score": int (0-10),
      "feedback": string,
      "suggestions": [string]
    }
  ],
  "top_strengths": [string],
  "critical_gaps": [string],
  "quick_wins": [string],
  "ats_analysis": {
    "ats_score": int (0-100),
    "missing_keywords": [string],
    "formatting_issues": [string]
  },
  "recruiter_verdict": string,
  "rewrite_hints": [string]
}
"""


def build_prompt(resume_text: str) -> str:
    return f"Review this resume:\n\n{resume_text}"




def call_llm(system: str, user: str) -> str:
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "temperature": 0.3,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            },
            timeout=60,
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"❌ API Request failed: {e}")



def extract_json(raw: str) -> dict:
    """
    Extract valid JSON even if model adds extra text.
    """
    raw = raw.strip()

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("❌ No JSON found in LLM output")

    json_str = raw[start:end + 1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Invalid JSON from LLM:\n{e}\n\n{raw}")



def review_resume(resume_text: str) -> ResumeReviewResult:
    raw_output = call_llm(
        system=SYSTEM_PROMPT,
        user=build_prompt(resume_text)
    )
    print(raw_output)
    parsed = extract_json(raw_output)
    print(parsed)

    try:
        return ResumeReviewResult(**parsed)
    except ValidationError as e:
        raise ValueError(f"❌ Validation failed:\n{e}")


